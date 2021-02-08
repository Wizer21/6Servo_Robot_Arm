import math
# FRONT AND UP
servo1pos = 1597 
servo2pos = 1690
# BACK AND UP  # PETIT ECART
#servo1pos = 797 
#servo2pos = 1712
# FRONT DOWN
#servo1pos = 2100 
#servo2pos = 1712

# self.servo_1 = servo_thread(self, pi, 1700, 1, [500, 2250]) # MORE IS DOWN
# self.servo_2 = servo_thread(self, pi, 2000, 2, [500, 2220]) # MORE IS DOWN
pi_rad = math.pi / 180

# TRIANGLE 1: X
width_1 = servo1pos
first_degrees = 180 - (width_1 - 500) / 9.722222
print("DEGREE " + str(first_degrees))

if first_degrees != 90:
    if first_degrees > 90: 
        is_first_part_frontward = False
        # THE ARM IS BACKWARD
        # TRIANGLE 1: X
        degrees = first_degrees - 90
        rad = degrees * pi_rad
        tri_1_y = math.cos(rad) * 10.5

        # TRIANGLE 1: Y
        third_angle  = 180 - (degrees + 90)
        rad = third_angle * pi_rad
        tri_1_x = math.cos(rad) * 10.5
    else:
        is_first_part_frontward = True
        # THE ARM IS FRONTWARD
        rad = first_degrees * pi_rad
        tri_1_x = math.cos(rad) * 10.5

        # TRIANGLE 1: Y
        third_angle = 180 - (first_degrees + 90)
        rad = third_angle * pi_rad
        tri_1_y = math.cos(rad) * 10.5       
else:
    third_angle = 90
    tri_1_y = 10.5
    tri_1_x = 0

width_2 = servo2pos
degrees = 180 - (width_2 - 500) / 9.5555555
print("degre arm2", str(degrees))

back_angle = first_degrees - ((first_degrees - 90) * 2)
#deg = degrees - 90
if degrees > back_angle:
    # SECOND PART HIGHT AND BACKWARD
    print("1")
    second_part_front = False            
    is_second_part_lower = False
    degrees -= back_angle

    # TRIANGLE 2: Y
    rad = degrees * pi_rad
    tri_2_y = math.cos(rad) * 10.5

    # TRIANGLE 2: X
    third_angle_tri_2 = 180 - (degrees + 90)
    rad = third_angle_tri_2 * pi_rad
    tri_2_x = math.cos(rad) * 10.5

elif degrees > 90 - first_degrees or not is_first_part_frontward: 
    # SECOND PART HIGHT AND FRONT
    print("2")
    is_second_part_lower = False
    second_part_front = True
    # TRIANGLE 2: X
    if not is_first_part_frontward:
        rec_degree = degrees + (first_degrees - 90)
    else:
        rec_degree = degrees - (90 - first_degrees)

    rad = rec_degree * pi_rad
    tri_2_x = math.cos(rad) * 10.5
    
    print("degrees", str(degrees))
    print("third_angle", str(third_angle))
    print("rec_degree", str(rec_degree))
    # TRIANGLE 2: Y
    third_angle_tri_2 = 180 - (rec_degree + 90)
    print("third_angle_tri_2", str(third_angle_tri_2))
    rad = third_angle_tri_2 * pi_rad
    tri_2_y = math.cos(rad) * 10.5
else: 
    print("3")
    # SECOND PART LOW AND FRONT
    second_part_front = True
    is_second_part_lower = True
    rec_degree = (90 + degrees) - third_angle
    third_angle_tri_2 = 180 - (rec_degree + 90)

    # TRIANGLE 2: X
    rad = third_angle_tri_2 * pi_rad
    tri_2_x = math.cos(rad) * 10.5

    # TRIANGLE 2: Y
    rad = rec_degree * pi_rad
    tri_2_y = math.cos(rad) * 10.5

print("tri_1_x", str(tri_1_x))
print("tri_2_x", str(tri_2_x))
print("tri_1_y", str(tri_1_y))
print("tri_2_y", str(tri_2_y))

if is_first_part_frontward and second_part_front:
    pos1 = round(tri_1_x + tri_2_x, 2)
elif not is_first_part_frontward and not second_part_front:
    pos1 = round(0 - (tri_2_x + tri_1_x), 2)        
elif not is_first_part_frontward and second_part_front:
    pos1 = round(tri_2_x - tri_1_x, 2)

if is_second_part_lower:
    pos2 = round(tri_1_y - tri_2_y, 2)
else:
    pos2 = round(tri_1_y + tri_2_y, 2)

claw_pos = [pos1, pos2]
print("INI POS = ", str(claw_pos))

if claw_pos[0] < 0:
    is_arm_front = False
    claw_pos[0] = -claw_pos[0]
else:
    is_arm_front = True


print("NEW POS = ", str(claw_pos))

#    M = motor  
#                         CLAW
#        M2  O--------------O
#           / \          -  |
#          /   \     -      |
#         /      X          |
#        /   -              |
#       / -                 |
#   M1 O ------------------ A

M1_X = (math.sqrt(claw_pos[0] ** 2 + claw_pos[1] ** 2)) / 2
print("M1_X", str(M1_X))

if M1_X >= 10.5:
    print("M1_X ADAPTED")
    M1_X = 10.4

M2_X = math.sqrt(10.5 ** 2 - M1_X ** 2)
print("M2_X", str(M2_X))

M2_M1_X_angle = (math.atan(M2_X / M1_X)) * 57.2958
print("M2_M1_X_angle", str(M2_M1_X_angle))
M1_M2_X_angle = 180 - (90 + M2_M1_X_angle)


X_M1_A_angle = (math.atan(claw_pos[1] / claw_pos[0])) * 57.2958
print("X_M1_A_angle", str(X_M1_A_angle))

M2_M1_A_angle = X_M1_A_angle + M2_M1_X_angle
M1_M2_CLAW_angle_minus_90 = (M1_M2_X_angle * 2) - 90

if not is_arm_front:
    angle_m1 = 180 - (X_M1_A_angle - M2_M1_X_angle)
    first_motor_width = 2250 - round(angle_m1 / 0.102857)
else:
    first_motor_width = 2250 - round(M2_M1_A_angle / 0.102857)
second_motor_width = 2220 - round(M1_M2_CLAW_angle_minus_90 / 0.104651)

print("M1_M2_X_angle", str(M1_M2_X_angle))
print("M2_M1_A_angle", str(M2_M1_A_angle))
print("M1_M2_CLAW_angle_minus_90", str(M1_M2_CLAW_angle_minus_90))

print("first_motor_width", str(first_motor_width), "second_motor_width", str(second_motor_width))


# self.servo_1 = servo_thread(self, pi, 1700, 1, [500, 2250]) # MORE IS DOWN
# self.servo_2 = servo_thread(self, pi, 2000, 2, [500, 2220]) # MORE IS DOWN