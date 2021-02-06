import math
# claw_pos = [14.9, 13.06] 1106 1716
# claw_pos = [14.9, 12.06] 1131 1805
claw_pos = [14.9, 8] 1146 2037

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

first_motor_width = 500 + round(M2_M1_A_angle / 0.1)
second_motor_width = 2200 - round(M1_M2_CLAW_angle_minus_90 / 0.10588)
print("first_motor_width " + str(first_motor_width))
print("second_motor_width " + str(second_motor_width))

print(str(first_motor_width) + " " + str(second_motor_width))