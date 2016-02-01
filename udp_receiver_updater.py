#!/usr/bin/env python
#
# nginx-updater.py - updates nginx proxy based on udp requests

from __future__ import print_function
import socket
import re
import time 
import os
from select import select
import itertools
import StringIO
import hashlib
import sys
import subprocess

class Request:
	"""Represents a proxy request that has been received by the program"""
	def __init__(self):
		self.service = ""
		self.host = ""
		self.port = 0
		self.timestamp = time.time()

class State:
	"""Represents the current request state which is used to update nginx"""
	def __init__(self):
		self.requestCt = 0
		self.requests = []
		self.last_modified = time.time()
		self.last_processed = time.time()
		self.last_gc = time.time()
		self.gc_interval = 5.0
		self.max_request_refresh_interval = 60.0

	def add_request(self, request):
		"""Add a request to the application state"""
		self.requestCt = self.requestCt + 1
		found = False
		for req in self.requests:
			if 	req.service == request.service and \
				req.host == req.host and \
				req.port == req.port:
					req.timestamp = request.timestamp
					found = True
					break
		if not found:
			self.requests.append(request)
			self.last_modified = time.time()

	def get_requests(self):
		"""Get the requests and reset last_process timestamp"""
		self.last_processed = self.last_modified
		return self.requests

	def gc_requests(self):
		"""Prune the request list of unrefreshed items"""
		now = time.time()
		if (now - self.last_gc) > self.gc_interval: 
			print('now: {0}'.format(now))
			for req in self.requests:
				print('req.timestamp: {0}'.format(req.timestamp))
				print('diff: {0}'.format(now - req.timestamp))
			live = [req for req in self.requests if (now - req.timestamp) < self.max_request_refresh_interval]
			dead = [req for req in self.requests if (now - req.timestamp) >= self.max_request_refresh_interval]

			if len(dead):
				self.requests = live
				self.last_modified = now

			self.last_gc = time.time()
	
	def modified(self):
		"""Have the requests been modified since they were last retrieved"""
		return self.last_modified > self.last_processed

def parse_buffer(data):
	"""Returns a sucessfully parsed and timestamped request or None"""
	m = re.match("([^;]+);([\d.]+);([\d]+)", data)
	if not m:
		print('Couldn''t grok request ''{0}'''.format(data), file=sys.stderr)
		return None

	req = Request()
	req.service = m.group(1)
	req.host = m.group(2)
	req.port = int(m.group(3))
	req.timestamp = time.time()

	return req

def canonical_request_dict(requests):
	"""A stable sorted set of current requirements"""
	key_func = lambda req: req.service
	service_key_func = lambda req: '{0}-{1}'.format(req.host,req.port)
	grouped_requests = sorted(requests, key=key_func)
	result = {}
	for k, g in itertools.groupby(grouped_requests, key_func):
    		result[k] = sorted(list(g), key=service_key_func)
	return result

def upstream_name(uri):
	"""Takes a service/uri location string and changes it into a upstream name"""
	return uri.strip("/").replace("/", "-")

def prepare_upstreams(requests):
	"""Prepare a nginx file with upstream directives - Expects a canonical request dict"""
	upstreams = StringIO.StringIO()

	upstreams.write('# Do not modify - this file is maintained by nginx_updater.py\n')
	for service, providers in requests.iteritems():
		upstreams.write('\nupstream {0} {{\n'.format(upstream_name(service)))
		for provider in providers:
			upstreams.write('\tserver {0}:{1} fail_timeout=10s;\n'.format(provider.host,provider.port))
		upstreams.write('}\n')
	
	return upstreams

def prepare_locations(requests):
	"""Prepare a nginx file with location directives - Expects a canonical request dict"""
	location = StringIO.StringIO()
	location.write('# Do not modify - this file is maintained by nginx_updater.py\n')
	for service in requests:
		location.write('\nlocation {0} {{\n'.format(service))
		location.write('\tproxy_pass http://{0}/;\n'.format(upstream_name(service)))
		location.write('\tproxy_redirect off;\n')
		location.write('\tproxy_next_upstream error timeout invalid_header http_500\n')
		location.write('\tproxy_connect_timeout 1s;\n')
		location.write('}\n')
	
	return location

def should_replace(new_content, current_location):
	"""Test to see if current content should be updated"""
	new_hash = hashlib.sha1()
	new_hash.update(new_content.getvalue())
	new_hash = new_hash.hexdigest()

	replace = False

	try:
		with open(current_location) as current:
			current_hash = hashlib.sha1()
			current_hash.update(current.read())
			current_hash = current_hash.hexdigest()
			if current_hash <> new_hash:
				replace = True
	except IOError:
		print('Exception while checking ''{0}'' content'.format(current_location), file=sys.stderr)
		replace = True

	return replace	

def replace_file(new_content, current_location):
	"""Atomically replaces file if new_content differs from
	   content at current_location"""
	if should_replace(new_content, current_location):
		abs_path = os.path.abspath(current_location)
		current_dir, filename = os.path.split(abs_path)
		tmp_filename = '{0}.{1}'.format(filename, time.time())
		tmp_path = os.path.join(current_dir, tmp_filename)

		try:
			with open(tmp_path, 'w') as tmp:
				tmp.write(new_content.getvalue())
			os.rename(tmp_path, abs_path)	
		except IOError:
			print('Failed to replace ''{0}'''.format(abs_path), file=sys.stderr)
			return False
		return True
	return False

def update_conf(requests, conf_dir):
	"""Updates configuration files that are intended for
	nginx"""
	canonical = canonical_request_dict(requests)
	locations = prepare_locations(canonical)
	upstreams = prepare_upstreams(canonical)

	locations_path = os.path.join(conf_dir, 'zorrillo-locations.conf')
	upstreams_path = os.path.join(conf_dir, 'zorrillo-upstreams.conf')

	locations_replaced = replace_file(locations, locations_path)
	upstreams_replaced = replace_file(upstreams, upstreams_path)

	if locations_replaced or upstreams_replaced:
		try:
			subprocess.check_call(['sudo', '/usr/sbin/nginx', 'reload'])
			print('NGINX reloaded')
		except (subprocess.CalledProcessError, OSError):
			print('Reloading NGINX failed', file=sys.stderr)

def nginx_updater(requests, conf_dir):
	"""Forked process that is responsible for updating nginx
	with the current requests"""
	newpid = os.fork()
	if newpid == 0:
		print('Contemplating {0} requests'.format(len(requests)))
		update_conf(requests, conf_dir)
		os._exit(0)
	else:
		return newpid


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description='udp listener that updates nginx configuration')
	parser.add_argument('-d', '--directory', help='Directory to maintain nginx configuration files in', required=True)
	parser.add_argument('-p', '--port', help='Port to listen for UDP requests on', required=True)

	args = parser.parse_args()
	args.port = int(args.port)

	udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_sock.bind(("0.0.0.0", args.port))

	updater_pid = 0
	state = State()

	start_time = time.time()

	print('Starting up, observing requests for 60s before applying updates...')

	# Sit in a loop aggregating requests and forking a process
	# to update the nginx configuration
	while True:
		input_ready,_,__ = select([udp_sock], [], [], 1.0)

		if input_ready:
			data, addr = udp_sock.recvfrom(1024)
			request = parse_buffer(data)
			if request:
				state.add_request(request)

		state.gc_requests()		

		if updater_pid == 0 and state.modified() and (time.time() - start_time > 60):
			updater_pid = nginx_updater(state.get_requests(), args.directory)

		if updater_pid:	
			pid, err_code = os.waitpid(updater_pid, os.WNOHANG)
			if pid <> 0:
				if err_code <> 0:
					print('updater exited with {0}'.format(err_code), file=sys.stderr)
				updater_pid = 0
