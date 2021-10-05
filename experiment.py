# -*- coding: utf-8 -*-

# TODO: begin checking/debugging mitigation functionality
# TODO: Double check how multi-session is handled by ANTI-VEA in OMEGA
# TODO: Test on OMEGA
# TODO: Revise experiment messages
# TODO: Rename project to reflect shift from compensatory to pursuit tracking

"""
Wondered if timestamps should be recorded in a format congruent w/ bioharness,
but might be fine as-is; timestamps currently recorded in epoch time,
which is easily convertable to standard date-time after the fact
"""



__author__ = "Brett Feltmate"

import sdl2.keycode
from klibs.KLCommunication import message
from sdl2 import SDL_GetKeyFromName, SDL_KEYDOWN, SDL_KEYUP, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDLK_SPACE
import random
import klibs
from klibs import P
from klibs.KLUserInterface import ui_request, any_key
from klibs.KLResponseCollectors import KeyPressResponse, KeyMap
from klibs.KLGraphics import *
from klibs.KLUtilities import *
from klibs.KLEventInterface import TrialEventTicket as TVT
from klibs.KLConstants import *
from klibs.KLKeyMap import KeyMap
from klibs.KLResponseCollectors import Response, KeyPressResponse
from sdl2 import *
from klibs.KLGraphics.KLNumpySurface import *
from CompTrack import *
import klibs.KLDatabase
import subprocess


from klibs.KLDatabase import EntryTemplate

class CompensatoryTrackingTask(klibs.Experiment):


	def setup(self):
		# Ensure display has been wiped before starting
		clear()
		flip()


		self.frames = []  # data for every screen refresh are captured and stored by trial

		# Ensure mouse-shake setting is disabled, as it will be triggered by mouse input
		if not P.development_mode:
			self.txtm.add_style('UserAlert', 16, (255, 000, 000))
			self.check_osx_mouse_shake_setting()

		# CompTrack class handles all events
		self.comp_track = CompTrack()
		self.comp_track.timeout_after = P.pvt_timeout
		# self.generate_ITIs()


		# Ensure mouse starts at centre and set invisible
		mouse_pos(False, P.screen_c)
		hide_mouse_cursor()

		# print('initial trials per block: {}'.format(P.trials_per_block))


		self.exp_messages = {
			'instrux':
				'In this task you will pursue a moving target (a white circle) by moving your cursor\n' +
				'(a green dot), with the goal of keeping your cursor centred within the target to the best of your ability.\n' +
				'You will control your cursor via the trackball provided to you.\n\n' +
				'At random intervals a large red timer will appear onscreen and begin counting upwards.\n' +
				'When this happens, press the spacebar key as quickly as possible to terminate it.\n' +
				'Upon termination of the timer, the pursuit task will immediately begin again.\n\n' +
				'If you have any questions please ask them now, and press spacebar when you are ready to proceed.',

			'progress': 'Beginning block {} of {}.\n',
			'break': 'Feel free to take a break at this time.',
			'meal': 'Meal break! The experiment will resume in approximately 30 minutes.',
			'complete': 'Task completed! Thank you! Press spacebar to exit the experiment.',
			'continue': '\n\nWhen you are ready, press spacebar to begin.'
		}


	def block(self):
		self.generate_ITIs()
		P.trials_per_block = len(self.itis)

		if P.session_number in [1, 7]:
			fill()
			message(self.exp_messages['instrux'], location=P.screen_c, registration=5)
			flip()
			any_key()

		# txt = self.exp_messages['progress'].format(P.block_number, P.blocks_per_experiment)
		#
		# if P.block_number > 1:
		# 	if P.block_number == 3:
		# 		txt += self.exp_messages['meal']
		# 	else:
		# 		txt += self.exp_messages['break']

		fill()
		message(self.exp_messages['continue'], location=P.screen_c, registration=5)
		flip()

		any_key()


	def setup_response_collector(self):
		pass

	def trial_prep(self):
		# Ensure mouse starts at centre and set invisible
		mouse_pos(False, P.screen_c)
		hide_mouse_cursor()

		self.comp_track.next_trial_start_time = now() + self.itis.pop()
		self.start = now()
		pump()

	def trial(self):
		start = now()
		rt = 0

		while now() < self.comp_track.next_trial_start_time + P.pvt_timeout and not rt:
			event_q = pump(True)
			ui_request(None, True, event_q)
			self.comp_track.refresh(event_q)
			if now() >= self.comp_track.next_trial_start_time:
				for event in event_q:
					if event.type == SDL_KEYDOWN:
						key = event.key.keysym
						if key.sym is sdl2.keycode.SDLK_SPACE:
							rt = now() - start
							break

		if not rt:
			# here's where we could  add feedback immediately after a lapse, were it desired
			pass
		self.comp_track.end_trial(rt)

		return {
			'session_num': P.session_number,
			'block_num': P.block_number,
			'trial_num' : P.trial_number,
			'timestamp': self.comp_track.current_frame.timestamp,
			'rt': self.comp_track.current_frame.rt
		}

	def trial_clean_up(self):
		pass

	def clean_up(self):
		for a in self.comp_track.assessments:
			self.db.insert(a.dump(), 'assessments')

		for trial in self.comp_track.frames:
			for f in trial:
				self.db.insert(f.dump(), 'frames')

		fill()
		message(self.exp_messages['complete'], location=P.screen_c, registration=5)
		flip()
		any_key()


	def check_osx_mouse_shake_setting(self):
		p = subprocess.Popen(
		"defaults read ~/Library/Preferences/.GlobalPreferences CGDisableCursorLocationMagnification 1", shell=True)

		if p == 0:
			fill((25, 25, 28))
			blit(NumpySurface(import_image_file('ExpAssets/Resources/image/accessibility_warning.png')), 5, P.screen_c)
			msg = 'Please ensure cursor shake-magnification is off before running this experiment.'
			x_pos = int((P.screen_y - 568) * 0.25) + 16
			message(msg, 'UserAlert', [P.screen_c[0], x_pos], 5)
			flip()
			any_key()
			quit()

	def generate_ITIs(self):
		block_trial_count = int(P.desired_block_duration / math.ceil(mean(P.iti) + 0.5))

		self.itis = np.random.randint(
			low=P.iti[0],
			high=P.iti[1] + 1,
			size=block_trial_count
		)

		if np.sum(np.add(self.itis, 0.5)) < P.desired_block_duration:
			while np.sum(np.add(self.itis, 0.5)) < P.desired_block_duration:
				iti = np.random.randint(
					low=P.iti[0],
					high=P.iti[1] + 1
				)
				self.itis = np.append(self.itis, iti)

		elif np.sum(np.add(self.itis, 0.5)) > P.desired_block_duration:
			while np.sum(np.add(self.itis, 0.5)) > P.desired_block_duration:
				self.itis = self.itis[:-1]

		self.itis = self.itis.tolist()

	@property
	def event_queue(self):
		return pump(True)

	def response_callback(self):
		self.rc.pvt_keyboard_response.responses[-1].append(self.frame_id())

	def event_label(self, event):
			return "trial_{}_{}".format(P.trial_number, event)

	def current_frame_id(self):
		return "{}:{}".format(P.trial_number - 1, len(self.frames[P.trial_number] - 1))


class PVTResponse(KeyPressResponse):
	__name__ = 'pvt_listener'

	def init(self):
		pass
		# self.__name__ = "pvt_listener"

	def listen(self, event_queue):
		for event in event_queue:
			if event.type == SDL_KEYDOWN:
				key = event.key.keysym # keyboard button event object
				ui_request(key) # check for ui requests (ie. quit, calibrate)
				if key == SDLK_SPACE:
					return Response(True, self.evm.trial_time_ms - self._rc_start)
				# if self.key_map.validate(key.sym):
				# 	value = self.key_map.read(key.sym, "data")
				# 	rt = (self.evm.trial_time_ms - self._rc_start)
				# 	return Response(value, rt)