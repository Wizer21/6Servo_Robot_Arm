import math
#servo1pos = 1102 
#servo2pos = 1705

servo1pos = 797 
servo2pos = 1712

pi_rad = math.pi / 180
is_second_part_lower = False

# TRIANGLE 1: X
width_1 = servo1pos
degrees = 90 - (width_1 - 500) / 10
print("deg ",str(degrees))
rad = degrees * pi_rad
tri_1_x = math.cos(rad) * 10.5
print("tri_1_x ",str(tri_1_x))

# TRIANGLE 1: Y
third_angle = 180 - (degrees + 90)
print("deg ",str(third_angle))
rad = third_angle * pi_rad
tri_1_y = math.cos(rad) * 10.5
print("tri_1_y ",str(tri_1_y))

width_2 = servo2pos
degrees = 180 - (width_2 - 500) / 9.4444

if degrees > third_angle: # 2nd part is higher
    print("hight")
    # TRIANGLE 2: X
    rec_degree = degrees - third_angle
    rad = rec_degree * pi_rad
    tri_2_x = math.cos(rad) * 10.5
    print("deg ",str(rec_degree))
    print("tri_2_x ",str(tri_2_x))
    
    # TRIANGLE 2: Y
    third_angle_tri_2 = 180 - (rec_degree + 90)
    print("deg ",str(third_angle_tri_2))
    rad = third_angle_tri_2 * pi_rad
    tri_2_y = math.cos(rad) * 10.5
    print("tri_2_y ",str(tri_2_y))
else: # 2nd part is lower
    print("low")
    is_second_part_lower = True
    rec_degree = (90 + degrees) - third_angle
    third_angle_tri_2 = 180 - (rec_degree + 90)
    print("deg ",str(rec_degree))
    print("deg ",str(third_angle_tri_2))

    # TRIANGLE 2: X
    rad = third_angle_tri_2 * pi_rad
    tri_2_x = math.cos(rad) * 10.5

    # TRIANGLE 2: Y
    rad = rec_degree * pi_rad
    tri_2_y = math.cos(rad) * 10.5

pos1 = round(tri_1_x + tri_2_x, 2)
if is_second_part_lower:
    pos2 = round(tri_1_y - tri_2_y, 2)
else:
    pos2 = round(tri_1_y + tri_2_y, 2)
arm_chord = [[tri_1_x, tri_1_y], [pos1, pos2]]

print("PARTI 1 POS " + str(arm_chord))

# claw_pos = [14.9, 13.06] 1106 1716
# claw_pos = [14.9, 12.06] 1131 1805
claw_pos = [arm_chord[1][0], arm_chord[1][1]] # 1146 2037
print("claw_pos " + str(claw_pos))

#    M = motor  
#                         CLAW
#        M2  O--------------O
#           / \          -  |
#          /   \     -      |
#         /      X          |
#        /   -              |
#       / -                 |
#   M1 O ------------------ A

# CALCULATE TANGENT: [0, 0] to claw
M1_X = (math.sqrt(claw_pos[0] ** 2 + claw_pos[1] ** 2)) / 2
print("M1_X " + str(M1_X))
X_M1_A_angle = (math.atan(claw_pos[1] / claw_pos[0])) * 57.2958
print("X_M1_A_angle " + str(X_M1_A_angle))

# CALCULATE MIDDLE POINT TO ELBOW POS
M2_X = math.sqrt(10.5 ** 2 - M1_X ** 2)
print("M2_X " + str(M2_X))
M2_M1_X_angle = (math.atan(M2_X / M1_X)) * 57.2958
print("M2_M1_X_angle " + str(M2_M1_X_angle))

# CALCULATE THIRD ANGLE OF THE SECOND RECTANGLE
M1_M2_X_angle = 180 - (90 + M2_M1_X_angle)
print("M1_M2_X_angle " + str(M1_M2_X_angle))

M2_M1_A_angle = X_M1_A_angle + M2_M1_X_angle
print("M2_M1_A_angle " + str(M2_M1_A_angle))
M1_M2_CLAW_angle_minus_90 = (M1_M2_X_angle * 2) - 90
print("M1_M2_CLAW_angle_minus_90 " + str(M1_M2_CLAW_angle_minus_90))

first_motor_width = 1400 - round(M2_M1_A_angle / 0.1)
second_motor_width = 2200 - round(M1_M2_CLAW_angle_minus_90 / 0.10588)
print("first_motor_width " + str(first_motor_width))
print("second_motor_width " + str(second_motor_width))

print(str(first_motor_width) + " " + str(second_motor_width))