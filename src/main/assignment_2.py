import numpy as np

#1

def nevilles_method(x_points, y_points, x):
    # must specify the matrix size (this is based on how many columns/rows you want)
    matrix = np.zeros((len(x_points), len(y_points)))
    ans = 0

    # fill in value (just the y values because we already have x set)
    for counter, row in enumerate(matrix):
        row[0] = y_points[counter]

    # the end of the first loop are how many columns you have...
    num_of_points = len(y_points)


    # populate final matrix (this is the iterative version of the recursion explained in class)
    # the end of the second loop is based on the first loop...
    for i in range(1, num_of_points):
        for j in range(1, i+1):
            first_multiplication = (x - x_points[i-j]) * matrix[i][j-1]
            second_multiplication = (x - x_points[i]) * matrix[i-1][j-1]

            denominator = x_points[i] - x_points[i-j]

            # this is the value that we will find in the matrix
            coefficient = (first_multiplication - second_multiplication) / denominator
            matrix[i][j] = coefficient
            ans = coefficient
            
    return ans



# point setup
x_points = [3.6, 3.8, 3.9]
y_points = [1.675, 1.436, 1.318]
approximating_value = 3.7
print(f"{nevilles_method(x_points, y_points, approximating_value)}\n")



#2

def divided_difference_table(x_points, y_points):
    # set up the matrix
    size = len(x_points)
    matrix = np.zeros((size, size))

    # fill the matrix
    for index, row in enumerate(matrix):
        row[0] = y_points[index]

    deg1 = 0
    deg2 = 0
    deg3 = 0
    k = 0
    # populate the matrix (end points are based on matrix size and max operations we're using)
    for i in range(1, size):
        for j in range(1, i+1):
            # the numerator are the immediate left and diagonal left indices...
            numerator = matrix[i][j-1] - matrix[i-1][j-1]

            # the denominator is the X-SPAN...
            denominator = x_points[i] - x_points[i-j]

            operation = numerator / denominator

            # cut it off to view it more simpler
            matrix[i][j] = operation
            if (i == j) and k == 0:
                deg1 = operation
                k += 1
            elif (i == j) and k == 1:
                deg2 = operation
                k += 1
            elif (i == j) and k == 2:
                deg3 = operation
                k += 1

    print(f"[{deg1}, {deg2}, {deg3}]\n")
    return matrix

# point setup
x_points = [7.2,7.4,7.5,7.6]
y_points = [23.5492, 25.3913,26.8224, 27.4589]
divided_table = divided_difference_table(x_points, y_points)



#3

def get_approximate_result(matrix, x_points, value):
    # p0 is always y0 and we use a reoccuring x to avoid having to recalculate x 
    reoccuring_x_span = 1
    reoccuring_px_result = matrix[0][0]
    
    # we only need the diagonals...and that starts at the first row...
    for index in range(0, 3):
        polynomial_coefficient = matrix[index+1][index+1]

        # we use the previous index for x_points....
        reoccuring_x_span *= (value - x_points[index])
        
        # get a_of_x * the x_span
        mult_operation = polynomial_coefficient * reoccuring_x_span

        # add the reoccuring px result
        reoccuring_px_result += mult_operation


    # final result
    return reoccuring_px_result

# find approximation
approximating_x = 7.3
print(f"{get_approximate_result(divided_table, x_points, approximating_x)}\n")



#4
np.set_printoptions(precision=7, suppress=True, linewidth=100)

def apply_div_dif(matrix):
    size = len(matrix)
    for i in range(2, size):
        for j in range(2, i+2):
            # skip if value is prefilled (we dont want to accidentally recalculate...)
            if j >= len(matrix[i]) or matrix[i][j] != 0:
                continue
            
            # get left cell entry
            left: float = matrix[i][j-1]

            # get diagonal left entry
            diagonal_left: float = matrix[i-1][j-1]

            # order of numerator is SPECIFIC.
            numerator: float = left - diagonal_left

            # denominator is current i's x_val minus the starting i's x_val....
            denominator = matrix[i][0] - matrix[i-j][0]

            # something save into matrix
            operation = numerator / denominator
            matrix[i][j] = operation
    
    return matrix

x_points = [3.6, 3.8, 3.9]
y_points = [1.675, 1.436, 1.318]
slopes = [-1.195, -1.188, -1.182]

# matrix size changes because of "doubling" up info for hermite 
num_of_points = len(x_points)
matrix = np.zeros(((2 * num_of_points), (2 * num_of_points)))

# populate x values (make sure to fill every TWO rows)
for x in range(0, num_of_points):
    matrix[2*x][0] = x_points[x]
    matrix[2*x+1][0] = x_points[x]
    
# prepopulate y values (make sure to fill every TWO rows)
for x in range(0, num_of_points):
    matrix[2*x][1] = y_points[x]
    matrix[2*x+1][1] = y_points[x]
    
# prepopulate with derivates (make sure to fill every TWO rows. starting row CHANGES.)
for x in range(0, num_of_points):
    matrix[2*x+1][2] = slopes[x]
    
filled_matrix = apply_div_dif(matrix)
print(filled_matrix)
print()



#5

x_points = [2, 5, 8, 10]
y_points = [3, 5, 7, 9]

base = np.zeros(4)
a_matrix = np.zeros((4,4))
b_matrix = np.zeros(4)

#a
for i in range(3):
    base[i] = x_points[i+1] - x_points[i]

a_matrix[0][0] = 1
a_matrix[1][0] = base[0]
a_matrix[1][1] = 2 * (base[0] + base[1])
a_matrix[1][2] = base[1]
a_matrix[2][1] = base[1]
a_matrix[2][2] = 2 * (base[1] + base[2])
a_matrix[2][3] = base[2]
a_matrix[3][3] = 1

print(f"{a_matrix}\n")

#b
b_matrix[1] = 3 / base[1] * (y_points[2] - y_points[1]) - 3 / h[0] * (y_points[1] - y_points[0])
b_matrix[2] = 3 / base[2] * (y_points[3] - y_points[2]) - 3 / h[1] * (y_points[2] - y_points[1])
print(f"{b_matrix}\n")

#c
x = np.linalg.inv(a_matrix).dot(b_matrix)
print(x)
