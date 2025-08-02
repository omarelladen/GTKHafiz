import csv

pb_line_width = 500  # lenght of line

exec(open('config').read())

with open(BAR_SIZES_FILE, mode='w') as file:
    writer = csv.writer(file)

    t_1 = 298
    s_1 = pb_line_width/t_1
    writer.writerow([1, 2, 291 * s_1])
    writer.writerow([1, 1, 7   * s_1])
    

    t_2 = 300
    s_2 = pb_line_width/t_2
    writer.writerow([2, 2, 300 * s_2])

    t_3 = 299.5
    s_3 = pb_line_width/t_3
    writer.writerow([3, 3, 179.5 * s_3])
    writer.writerow([3, 2, 120   * s_3])

    t_4 = 296.5
    s_4 = pb_line_width/t_4
    writer.writerow([4, 4, 74    * s_4])
    writer.writerow([4, 3, 222.5 * s_4])

    t_5 = 300
    s_5 = pb_line_width/t_5
    writer.writerow([5, 4, 300 * s_5])

    t_6 = 291.5
    s_6 = pb_line_width/t_6
    writer.writerow([6, 5, 226.5 * s_6])
    writer.writerow([6, 4, 65    * s_6])

    t_7 = 304.5
    s_7 = pb_line_width/t_7
    writer.writerow([7, 6, 208  * s_7])
    writer.writerow([7, 5, 96.5 * s_7])

    t_8 = 298
    s_8 = pb_line_width/t_8
    writer.writerow([8, 7, 163 * s_8])
    writer.writerow([8, 6, 135 * s_8])

    t_9 = 298
    s_9 = pb_line_width/t_9
    writer.writerow([9, 8, 73  * s_9])
    writer.writerow([9, 7, 225 * s_9])

    t_10 = 296.5
    s_10 = pb_line_width/t_10
    writer.writerow([10, 9, 221.5 * s_10])
    writer.writerow([10, 8, 75    * s_10])

    t_11 = 298.5
    s_11 = pb_line_width/t_11
    writer.writerow([11, 11, 7    * s_11])
    writer.writerow([11, 10, 200  * s_11])
    writer.writerow([11, 9, 91.5 * s_11])

    t_12 = 298
    s_12 = pb_line_width/t_12
    writer.writerow([12, 12, 95  * s_12])
    writer.writerow([12, 11, 203 * s_12])

    t_13 = 296
    s_13 = pb_line_width/t_13
    writer.writerow([13, 14, 101 * s_13])
    writer.writerow([13, 13, 90  * s_13])
    writer.writerow([13, 12, 105 * s_13])

    t_14 = 296
    s_14 = pb_line_width/t_14
    writer.writerow([14, 16, 217 * s_14])
    writer.writerow([14, 15, 79  * s_14])

    t_15 = 296
    s_15 = pb_line_width/t_15
    writer.writerow([15, 18, 124 * s_15])
    writer.writerow([15, 17, 172 * s_15])

    t_16 = 296
    s_16 = pb_line_width/t_16
    writer.writerow([16, 20, 144 * s_16])
    writer.writerow([16, 19, 107 * s_16])
    writer.writerow([16, 18, 45  * s_16])

    t_17 = 295
    s_17 = pb_line_width/t_17
    writer.writerow([17, 22, 148 * s_17])
    writer.writerow([17, 21, 147 * s_17])

    t_18 = 295
    s_18 = pb_line_width/t_18
    writer.writerow([18, 25, 33  * s_18])
    writer.writerow([18, 24, 144 * s_18])
    writer.writerow([18, 23, 118 * s_18])

    t_19 = 296
    s_19 = pb_line_width/t_19
    writer.writerow([19, 27, 74  * s_19])
    writer.writerow([19, 26, 148 * s_19])
    writer.writerow([19, 25, 74  * s_19])

    t_20 = 296
    s_20 = pb_line_width/t_20
    writer.writerow([20, 29, 81  * s_20])
    writer.writerow([20, 28, 163 * s_20])
    writer.writerow([20, 27, 52  * s_20])

    t_21 = 292
    s_21 = pb_line_width/t_21
    writer.writerow([21, 33, 59 * s_21])
    writer.writerow([21, 32, 43 * s_21])
    writer.writerow([21, 31, 57 * s_21])
    writer.writerow([21, 30, 94 * s_21])
    writer.writerow([21, 29, 39 * s_21])

    t_22 = 294
    s_22 = pb_line_width/t_22
    writer.writerow([22, 36, 25 * s_22])
    writer.writerow([22, 35, 84 * s_22])
    writer.writerow([22, 34, 95 * s_22])
    writer.writerow([22, 33, 90 * s_22])

    t_23 = 294
    s_23 = pb_line_width/t_23
    writer.writerow([23, 39, 55  * s_23])
    writer.writerow([23, 38, 77  * s_23])
    writer.writerow([23, 37, 103 * s_23])
    writer.writerow([23, 36, 59  * s_23])

    t_24 = 296
    s_24 = pb_line_width/t_24
    writer.writerow([24, 41, 73  * s_24])
    writer.writerow([24, 40, 146 * s_24])
    writer.writerow([24, 39, 77  * s_24])

    t_25 = 298
    s_25 = pb_line_width/t_25
    writer.writerow([25, 45, 50 * s_25])
    writer.writerow([25, 44, 42 * s_25])
    writer.writerow([25, 43, 99 * s_25])
    writer.writerow([25, 42, 92 * s_25])
    writer.writerow([25, 41, 15 * s_25])

    t_26 = 282
    s_26 = pb_line_width/t_26
    writer.writerow([26, 51, 17 * s_26])
    writer.writerow([26, 50, 39 * s_26])
    writer.writerow([26, 49, 37 * s_26])
    writer.writerow([26, 48, 64 * s_26])
    writer.writerow([26, 47, 59 * s_26])
    writer.writerow([26, 46, 66 * s_26])

    t_27 = 288
    s_27 = pb_line_width/t_27
    writer.writerow([27, 57, 63 * s_27])
    writer.writerow([27, 56, 47 * s_27])
    writer.writerow([27, 55, 45 * s_27])
    writer.writerow([27, 54, 38 * s_27])
    writer.writerow([27, 53, 38 * s_27])
    writer.writerow([27, 52, 35 * s_27])
    writer.writerow([27, 51, 22 * s_27])

    t_28 = 282
    s_28 = pb_line_width/t_28
    writer.writerow([28, 66, 28 * s_28])
    writer.writerow([28, 65, 29 * s_28])
    writer.writerow([28, 64, 28 * s_28])
    writer.writerow([28, 63, 21 * s_28])
    writer.writerow([28, 62, 19 * s_28])
    writer.writerow([28, 61, 22 * s_28])
    writer.writerow([28, 60, 35 * s_28])
    writer.writerow([28, 59, 51 * s_28])
    writer.writerow([28, 58, 49 * s_28])

    t_29 = 278
    s_29 = pb_line_width/t_29
    writer.writerow([29, 77, 22 * s_29])
    writer.writerow([29, 76, 25 * s_29])
    writer.writerow([29, 75, 17 * s_29])
    writer.writerow([29, 74, 26 * s_29])
    writer.writerow([29, 73, 20 * s_29])
    writer.writerow([29, 72, 28 * s_29])
    writer.writerow([29, 71, 24 * s_29])
    writer.writerow([29, 70, 24 * s_29])
    writer.writerow([29, 69, 27 * s_29])
    writer.writerow([29, 68, 32 * s_29])
    writer.writerow([29, 67, 33 * s_29])

    t_30 = 271
    s_30 = pb_line_width/t_30
    writer.writerow([30, 114, 4  * s_30])
    writer.writerow([30, 113, 3  * s_30])
    writer.writerow([30, 112, 2  * s_30])
    writer.writerow([30, 111, 3  * s_30])
    writer.writerow([30, 110, 3  * s_30])
    writer.writerow([30, 109, 3  * s_30])
    writer.writerow([30, 108, 2  * s_30])
    writer.writerow([30, 107, 4  * s_30])
    writer.writerow([30, 106, 3  * s_30])
    writer.writerow([30, 105, 3  * s_30])
    writer.writerow([30, 104, 4  * s_30])
    writer.writerow([30, 103, 2  * s_30])
    writer.writerow([30, 102, 3  * s_30])
    writer.writerow([30, 101, 5  * s_30])
    writer.writerow([30, 100, 5  * s_30])
    writer.writerow([30, 99, 4  * s_30])
    writer.writerow([30, 98, 10 * s_30])
    writer.writerow([30, 97, 3  * s_30])
    writer.writerow([30, 96, 8  * s_30])
    writer.writerow([30, 95, 4  * s_30])
    writer.writerow([30, 94, 3  * s_30])
    writer.writerow([30, 93, 5  * s_30])
    writer.writerow([30, 92, 8  * s_30])
    writer.writerow([30, 91, 7  * s_30])
    writer.writerow([30, 90, 9  * s_30])
    writer.writerow([30, 89, 16 * s_30])
    writer.writerow([30, 88, 11 * s_30])
    writer.writerow([30, 87, 8  * s_30])
    writer.writerow([30, 86, 7  * s_30])
    writer.writerow([30, 85, 12 * s_30])
    writer.writerow([30, 84, 12 * s_30])
    writer.writerow([30, 83, 19 * s_30])
    writer.writerow([30, 82, 9  * s_30])
    writer.writerow([30, 81, 12 * s_30])
    writer.writerow([30, 80, 15 * s_30])
    writer.writerow([30, 79, 20 * s_30])
    writer.writerow([30, 78, 20 * s_30])
