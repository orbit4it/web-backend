# TODO
# 1. create_schedule : bikin row data baru dengan parameter skema
#                     - exception value token harus unique tidak boleh ada duplikat
# 2. edit_schedule : ubah row data dengan parameter id dan skema
# 3. del_schedule : hapus row data dengan parameter id
# 4. toggle_attendance_open : ubah value attendance_is_open menjadi False maupun True dengan parameter id

import strawberry


@strawberry.type
class Mutation:
    ...
