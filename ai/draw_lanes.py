import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq
from statistics import mean

def draw_lanes(image, lines, color=[0,255,255], thickness=3):
	# if this fails go with some default lines
	try:
		# find the max y value for a lane marker
		# since we ecannoot assume horizon will always be at the same point

		ys = []
		for line in lines:
			for i in line:
				ys += [i[1], i[3]]
		min_y = min(ys)
		max_y = 600
		new_lines = []
		line_dict = {}

		for idx, i in enumerate(lines):
			for xyxy in i:
				# These four lines:
				# Used to caluclate definition from a  line
				x_coords = (xyxy[0], xyxy[2])
				y_coords = (xyxy[1], xyxy[3])
				A = vstack([x_coords, ones(len(x_coords))]).T
				m, b = lstsq(A, y_coords)[0]

				# Calculating new nad imporved xs
				x1 = (min_y - b) / m
				x2 = (max_y - b) / m

				line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]
				new_lines.append([int(x1), min_y, int(x2), max_y])

		final_lanes = {}

		# check for the slope, want to  find lines with similar slope
		for idx in line_dict:
			final_lanes_copy = final_lanes.copy()
			m = line_dict[idx][0]
			b = line_dict[idx][1]
			line = line_dict[idx][2]

			if len(final_lanes) == 0:
				final_lanes[m] = [[m, b, line]]
			else:
				found_copy = False

				for other_ms in final_lanes_copy:
					if not found_copy:
						if abs(other_ms * 1.1) > abs(m) > abs(other_ms * 0.9):
							if abs(final_lanes_copy[other_ms][0][1] * 1.1) > abs(b) > abs(final_lanes_copy[other_ms][0][1] * 0.9):
								final_lanes[other_ms].append([m, b, line])
								found_copy = True
								break
						else:
							final_lanes[m] = [[m, b, line]]

		line_counter = {}

		for lanes in final_lanes:
			line_counter[lanes] = len(final_lanes[lanes])

		top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

		lane1_id = top_lanes[0][0]
		lane2_id = top_lanes[1][0]

		def average_lane(lane_data):
			x1s = []
			y1s = []
			x2s = []
			y2s = []
			for data in lane_data:
				x1s.append(data[2][0])
				y1s.append(data[2][1])
				x2s.append(data[2][2])
				y2s.append(data[2][3])
			return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 

		l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
		l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

		return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
	except Exception as e:
		print(str(e))
