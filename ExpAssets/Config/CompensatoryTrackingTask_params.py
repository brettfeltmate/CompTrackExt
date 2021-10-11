### Klibs Parameter overrides ###

#########################################
# Runtime Settings
#########################################
collect_demographics = True
manual_demographics_collection = False
manual_trial_generation = True
run_practice_blocks = False
multi_user = False
view_distance = 57 # in centimeters, 57cm = 1 deg of visual angle per cm of screen

#########################################
# Available Hardware
#########################################
eye_tracker_available = False
eye_tracking = False

#########################################
# Environment Aesthetic Defaults
#########################################
default_fill_color = (45, 45, 45, 255)
default_color = (255, 255, 255, 255)
default_font_size = 23
default_font_unit = 'px'
default_font_name = 'Hind-Medium'

#########################################
# EyeLink Settings
#########################################
manual_eyelink_setup = False
manual_eyelink_recording = False

saccadic_velocity_threshold = 20
saccadic_acceleration_threshold = 5000
saccadic_motion_threshold = 0.15

#########################################
# Experiment Structure
#########################################
multi_session_project = True
trials_per_block = 0
blocks_per_experiment = 0
table_defaults = {}
conditions = []
default_condition = None

#########################################
# Development Mode Settings
#########################################
dm_auto_threshold = True
dm_trial_show_mouse = True
dm_ignore_local_overrides = False
dm_show_gaze_dot = True

#########################################
# Data Export Settings
#########################################
primary_table = "trials"
unique_identifier = "userhash"
exclude_data_cols = ["created"]
append_info_cols = ["random_seed"]
datafile_ext = ".txt"

#########################################
# PROJECT-SPECIFIC VARS
#########################################
iti = [2, 8]  		# s, min/max
rt_lapse_criterion = 1000 	# s
desired_block_duration = 30 	# s
poll_while_moving = True
poll_at_fixation = False
reset_target_after_poll = True
assessment_sample_size = 5
supervise_input = False
max_input_step = 5  # ie. is input is supervised, this is the threshld initiating it, in pixels-travlled-per-frame
excessive_lapse_threshold = 3  # in number of lapses per assessment window
max_mean_rt = 0.5
assessing = {'lapses':True, 'mean_rt': True}
audio_warning_file_path = None
audio_warning_duration = 0
pause_duration = 5
pausing_clears_screen = False
pause_targets = True
ramp_factors = []
session_number = 1
