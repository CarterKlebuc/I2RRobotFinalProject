import math

pen_up = 0.3064
pen_down = 0.3264


a_values = [
    (0, 1, pen_down),
    (-1, -1, pen_down),
    (-1, -1, pen_up),
    (0, 1, pen_up),
    (0, 1, pen_down),
    (1, -1, pen_down),
    (1, -1, pen_up),
    (-0.5, 0, pen_up),
    (-0.5, 0, pen_down),
    (0.5, 0, pen_down)
]

b_values = [
    (-1, 1, pen_down),
    (1, 1, pen_down),
    (1, 0.2, pen_down),
    (-1, 0.2, pen_down),
    (-1, 0, pen_down),
    (-1, -0.2, pen_down),
    (1, -0.2, pen_down),
    (1, -1, pen_down),
    (-1, -1, pen_down),
    (-1, 0, pen_down)
]



c_values = [
    (1 * math.cos(math.radians(45)), 1 * math.sin(math.radians(45)), pen_down),
    (1 * math.cos(math.radians(60)), 1 * math.sin(math.radians(60)), pen_down),
    (1 * math.cos(math.radians(75)), 1 * math.sin(math.radians(75)), pen_down),
    (1 * math.cos(math.radians(90)), 1 * math.sin(math.radians(90)), pen_down),
    (1 * math.cos(math.radians(105)), 1 * math.sin(math.radians(105)), pen_down),
    (1 * math.cos(math.radians(120)), 1 * math.sin(math.radians(120)), pen_down),
    (1 * math.cos(math.radians(135)), 1 * math.sin(math.radians(135)), pen_down),
    (1 * math.cos(math.radians(150)), 1 * math.sin(math.radians(150)), pen_down),
    (1 * math.cos(math.radians(165)), 1 * math.sin(math.radians(165)), pen_down),
    (1 * math.cos(math.radians(180)), 1 * math.sin(math.radians(180)), pen_down),
    (1 * math.cos(math.radians(195)), 1 * math.sin(math.radians(195)), pen_down),
    (1 * math.cos(math.radians(210)), 1 * math.sin(math.radians(210)), pen_down),
    (1 * math.cos(math.radians(225)), 1 * math.sin(math.radians(225)), pen_down),
    (1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240)), pen_down),
    (1 * math.cos(math.radians(255)), 1 * math.sin(math.radians(255)), pen_down),
    (1 * math.cos(math.radians(270)), 1 * math.sin(math.radians(270)), pen_down),
    (1 * math.cos(math.radians(285)), 1 * math.sin(math.radians(285)), pen_down),
    (1 * math.cos(math.radians(315)), 1 * math.sin(math.radians(315)), pen_down),
]

d_values = [
    (-1, 1, pen_down),
    (-1, -1, pen_down),
    (-1, -1, pen_up),
    (-1, 1, pen_up),
    (-1, 1, pen_down),
    (0, 1, pen_down),
    (0, 1, pen_up),
    (-1, -1, pen_up),
    (-1, -1, pen_down),
    (0, 1, pen_down),
    (1 * math.cos(math.radians(270)), 1 * math.sin(math.radians(270)), pen_down),
    (1 * math.cos(math.radians(285)), 1 * math.sin(math.radians(285)), pen_down),
    (1 * math.cos(math.radians(315)), 1 * math.sin(math.radians(315)), pen_down),
    (1 * math.cos(math.radians(330)), 1 * math.sin(math.radians(330)), pen_down),
    (1 * math.cos(math.radians(345)), 1 * math.sin(math.radians(345)), pen_down),
    (1 * math.cos(math.radians(360)), 1 * math.sin(math.radians(360)), pen_down),
    (1 * math.cos(math.radians(0)), 1 * math.sin(math.radians(0)), pen_down),
    (1 * math.cos(math.radians(15)), 1 * math.sin(math.radians(15)), pen_down),
    (1 * math.cos(math.radians(30)), 1 * math.sin(math.radians(30)), pen_down),
    (1 * math.cos(math.radians(45)), 1 * math.sin(math.radians(45)), pen_down),
    (1 * math.cos(math.radians(60)), 1 * math.sin(math.radians(60)), pen_down),
    (1 * math.cos(math.radians(75)), 1 * math.sin(math.radians(75)), pen_down),
    (1 * math.cos(math.radians(90)), 1 * math.sin(math.radians(90)), pen_down),
]

e_values = [
    (-1, 1, pen_down),
    (1, 1, pen_down),
    (1, 1, pen_up),
    (-1, 1, pen_up),
    (-1, 0, pen_down),
    (1, 0, pen_down),
    (1, 0, pen_up),
    (-1, 0, pen_up),
    (-1, -1, pen_down),
    (1, -1, pen_down),
]

f_values = [
    (-1, 1, pen_down),
    (1, 1, pen_down),
    (1, 1, pen_up),
    (-1, 1, pen_up),
    (-1, 0, pen_down),
    (1, 0, pen_down),
    (1, 0, pen_up),
    (-1, 0, pen_up),
    (-1, -1, pen_down),
]

g_values = [
    (1 * math.cos(math.radians(60)), 1 * math.sin(math.radians(60)), pen_down),
    (1 * math.cos(math.radians(75)), 1 * math.sin(math.radians(75)), pen_down),
    (1 * math.cos(math.radians(90)), 1 * math.sin(math.radians(90)), pen_down),
    (1 * math.cos(math.radians(105)), 1 * math.sin(math.radians(105)), pen_down),
    (1 * math.cos(math.radians(120)), 1 * math.sin(math.radians(120)), pen_down),
    (1 * math.cos(math.radians(135)), 1 * math.sin(math.radians(135)), pen_down),
    (1 * math.cos(math.radians(150)), 1 * math.sin(math.radians(150)), pen_down),
    (1 * math.cos(math.radians(165)), 1 * math.sin(math.radians(165)), pen_down),
    (1 * math.cos(math.radians(180)), 1 * math.sin(math.radians(180)), pen_down),
    (1 * math.cos(math.radians(195)), 1 * math.sin(math.radians(195)), pen_down),
    (1 * math.cos(math.radians(210)), 1 * math.sin(math.radians(210)), pen_down),
    (1 * math.cos(math.radians(225)), 1 * math.sin(math.radians(225)), pen_down),
    (1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240)), pen_down),
    (1 * math.cos(math.radians(255)), 1 * math.sin(math.radians(255)), pen_down),
    (1 * math.cos(math.radians(270)), 1 * math.sin(math.radians(270)), pen_down),
    (1 * math.cos(math.radians(285)), 1 * math.sin(math.radians(285)), pen_down),
    (1 * math.cos(math.radians(315)), 1 * math.sin(math.radians(315)), pen_down),
    (1 * math.cos(math.radians(330)), 1 * math.sin(math.radians(330)), pen_down),
    (1 * math.cos(math.radians(345)), 1 * math.sin(math.radians(345)), pen_down),
    (1 * math.cos(math.radians(360)), 1 * math.sin(math.radians(360)), pen_down),
    (0, 0, pen_down)
]

h_values = [
    (-1, 1, pen_down),
    (-1, -1, pen_down),
    (-1, -1, pen_up),
    (-1, 0, pen_up),
    (-1, 0, pen_down),
    (1, 0, pen_down),
    (1, 0, pen_up),
    (1, 1, pen_up),
    (1, 1, pen_down),
    (1, -1, pen_down),
]

i_values = [
    (-1, 1, pen_down),
    (1, 1, pen_down),
    (1, 1, pen_up),
    (0, 1, pen_up),
    (0, 1, pen_down),
    (0, -1, pen_down),
    (0, -1, pen_up),
    (-1, -1, pen_up),
    (-1, -1, pen_down),
    (1, -1, pen_down)
]

j_values = [
    (1 * math.cos(math.radians(180)), 1 * math.sin(math.radians(180)), pen_down),
    (1 * math.cos(math.radians(195)), 1 * math.sin(math.radians(195)), pen_down),
    (1 * math.cos(math.radians(210)), 1 * math.sin(math.radians(210)), pen_down),
    (1 * math.cos(math.radians(225)), 1 * math.sin(math.radians(225)), pen_down),
    (1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240)), pen_down),
    (1 * math.cos(math.radians(255)), 1 * math.sin(math.radians(255)), pen_down),
    (1 * math.cos(math.radians(270)), 1 * math.sin(math.radians(270)), pen_down),
    (1 * math.cos(math.radians(285)), 1 * math.sin(math.radians(285)), pen_down),
    (1 * math.cos(math.radians(315)), 1 * math.sin(math.radians(315)), pen_down),
    (1 * math.cos(math.radians(330)), 1 * math.sin(math.radians(330)), pen_down),
    (1 * math.cos(math.radians(345)), 1 * math.sin(math.radians(345)), pen_down),
    (1 * math.cos(math.radians(360)), 1 * math.sin(math.radians(360)), pen_down),
    (1, 1, pen_down),
    (-1, 1, pen_down)
]

k_values = [
    (-1, 1, pen_down),
    (-1, -1, pen_down),
    (-1, -1, pen_up),
    (-1, 0, pen_up),
    (-1, 0, pen_down),
    (1, 1, pen_down),
    (1, 1, pen_up),
    (-1, 0, pen_up),
    (-1, 0, pen_down),
    (1, -1, pen_down),
]

l_values = [
    (-1, 1, pen_down),
    (-1, -1.5, pen_down),
    (1, -1.5, pen_down)
]

m_values = [
    (0, -1, pen_down),
    (1, 1, pen_down),
    (1, -1, pen_down),
    (1, -1, pen_up),
    (0, -1, pen_up),
    (0, -1, pen_down),
    (-1, 1, pen_down),
    (-1, -1, pen_down)
]

n_values = [
    (-1, 1, pen_down),
    (1, -1, pen_down),
    (1, 1, pen_down)
]

o_values = [
    (1 * math.cos(math.radians(0)), 1 * math.sin(math.radians(0)), pen_down),
    (1 * math.cos(math.radians(15)), 1 * math.sin(math.radians(15)), pen_down),
    (1 * math.cos(math.radians(30)), 1 * math.sin(math.radians(30)), pen_down),
    (1 * math.cos(math.radians(45)), 1 * math.sin(math.radians(45)), pen_down),
    (1 * math.cos(math.radians(60)), 1 * math.sin(math.radians(60)), pen_down),
    (1 * math.cos(math.radians(75)), 1 * math.sin(math.radians(75)), pen_down),
    (1 * math.cos(math.radians(90)), 1 * math.sin(math.radians(90)), pen_down),
    (1 * math.cos(math.radians(105)), 1 * math.sin(math.radians(105)), pen_down),
    (1 * math.cos(math.radians(120)), 1 * math.sin(math.radians(120)), pen_down),
    (1 * math.cos(math.radians(135)), 1 * math.sin(math.radians(135)), pen_down),
    (1 * math.cos(math.radians(150)), 1 * math.sin(math.radians(150)), pen_down),
    (1 * math.cos(math.radians(165)), 1 * math.sin(math.radians(165)), pen_down),
    (1 * math.cos(math.radians(180)), 1 * math.sin(math.radians(180)), pen_down),
    (1 * math.cos(math.radians(195)), 1 * math.sin(math.radians(195)), pen_down),
    (1 * math.cos(math.radians(210)), 1 * math.sin(math.radians(210)), pen_down),
    (1 * math.cos(math.radians(225)), 1 * math.sin(math.radians(225)), pen_down),
    (1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240)), pen_down),
    (1 * math.cos(math.radians(255)), 1 * math.sin(math.radians(255)), pen_down),
    (1 * math.cos(math.radians(270)), 1 * math.sin(math.radians(270)), pen_down),
    (1 * math.cos(math.radians(285)), 1 * math.sin(math.radians(285)), pen_down),
    (1 * math.cos(math.radians(315)), 1 * math.sin(math.radians(315)), pen_down),
    (1 * math.cos(math.radians(330)), 1 * math.sin(math.radians(330)), pen_down),
    (1 * math.cos(math.radians(345)), 1 * math.sin(math.radians(345)), pen_down),
    (1 * math.cos(math.radians(360)), 1 * math.sin(math.radians(360)), pen_down),
]

p_values = [
    (-1, 1, pen_down),
    (1, 1, pen_down),
    (1, 0, pen_down),
    (-1, 0, pen_down),
    (-1, -1, pen_down)
]

q_values = [
    (1 * math.cos(math.radians(0)), 1 * math.sin(math.radians(0)), pen_down),
    (1 * math.cos(math.radians(15)), 1 * math.sin(math.radians(15)), pen_down),
    (1 * math.cos(math.radians(30)), 1 * math.sin(math.radians(30)), pen_down),
    (1 * math.cos(math.radians(45)), 1 * math.sin(math.radians(45)), pen_down),
    (1 * math.cos(math.radians(60)), 1 * math.sin(math.radians(60)), pen_down),
    (1 * math.cos(math.radians(75)), 1 * math.sin(math.radians(75)), pen_down),
    (1 * math.cos(math.radians(90)), 1 * math.sin(math.radians(90)), pen_down),
    (1 * math.cos(math.radians(105)), 1 * math.sin(math.radians(105)), pen_down),
    (1 * math.cos(math.radians(120)), 1 * math.sin(math.radians(120)), pen_down),
    (1 * math.cos(math.radians(135)), 1 * math.sin(math.radians(135)), pen_down),
    (1 * math.cos(math.radians(150)), 1 * math.sin(math.radians(150)), pen_down),
    (1 * math.cos(math.radians(165)), 1 * math.sin(math.radians(165)), pen_down),
    (1 * math.cos(math.radians(180)), 1 * math.sin(math.radians(180)), pen_down),
    (1 * math.cos(math.radians(195)), 1 * math.sin(math.radians(195)), pen_down),
    (1 * math.cos(math.radians(210)), 1 * math.sin(math.radians(210)), pen_down),
    (1 * math.cos(math.radians(225)), 1 * math.sin(math.radians(225)), pen_down),
    (1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240)), pen_down),
    (1 * math.cos(math.radians(255)), 1 * math.sin(math.radians(255)), pen_down),
    (1 * math.cos(math.radians(270)), 1 * math.sin(math.radians(270)), pen_down),
    (1 * math.cos(math.radians(285)), 1 * math.sin(math.radians(285)), pen_down),
    (1 * math.cos(math.radians(315)), 1 * math.sin(math.radians(315)), pen_down),
    (1 * math.cos(math.radians(330)), 1 * math.sin(math.radians(330)), pen_down),
    (1 * math.cos(math.radians(345)), 1 * math.sin(math.radians(345)), pen_down),
    (1 * math.cos(math.radians(360)), 1 * math.sin(math.radians(360)), pen_down),
    (1 * math.cos(math.radians(360)), 1 * math.sin(math.radians(360)), pen_up),
    (0, 0, pen_up),
    (0, 0, pen_down),
    (1, -1, pen_down)
]

r_values = [
    (-1, 1, pen_down),
    (-1, -1, pen_down),
    (-1, -1, pen_up),
    (-1, 0, pen_up),
    (-1, 0, pen_down),
    (1, -1, pen_down),
    (1, -1, pen_up),
    (-1, 1, pen_up),
    (-1, 1, pen_down),
    (1, 1, pen_down),
    (1, 0, pen_down),
    (-1, 0, pen_down)
]

s_values = [
    (1 * math.cos(math.radians(0)), 1 * math.sin(math.radians(0)) + 0.5, pen_down),
    (1 * math.cos(math.radians(15)), 1 * math.sin(math.radians(15)) + 0.5, pen_down),
    (1 * math.cos(math.radians(30)), 1 * math.sin(math.radians(30)) + 0.5, pen_down),
    (1 * math.cos(math.radians(45)), 1 * math.sin(math.radians(45)) + 0.5, pen_down),
    (1 * math.cos(math.radians(60)), 1 * math.sin(math.radians(60)) + 0.5, pen_down),
    (1 * math.cos(math.radians(75)), 1 * math.sin(math.radians(75)) + 0.5, pen_down),
    (1 * math.cos(math.radians(90)), 1 * math.sin(math.radians(90)) + 0.5, pen_down),
    (1 * math.cos(math.radians(105)), 1 * math.sin(math.radians(105)) + 0.5, pen_down),
    (1 * math.cos(math.radians(120)), 1 * math.sin(math.radians(120)) + 0.5, pen_down),
    (1 * math.cos(math.radians(135)), 1 * math.sin(math.radians(135)) + 0.5, pen_down),
    (1 * math.cos(math.radians(150)), 1 * math.sin(math.radians(150)) + 0.5, pen_down),
    (1 * math.cos(math.radians(165)), 1 * math.sin(math.radians(165)) + 0.5, pen_down),
    (1 * math.cos(math.radians(180)), 1 * math.sin(math.radians(180)) + 0.5, pen_down),
    (1 * math.cos(math.radians(195)), 1 * math.sin(math.radians(195)) + 0.5, pen_down),
    (1 * math.cos(math.radians(195)), 1 * math.sin(math.radians(195)) + 0.5, pen_down),

    (1 * math.cos(math.radians(15)), 1 * math.sin(math.radians(15)) - 0.5, pen_down),
    (1 * math.cos(math.radians(15)), 1 * math.sin(math.radians(15)) - 0.5, pen_down),
    (1 * math.cos(math.radians(360)), 1 * math.sin(math.radians(360)) - 0.5, pen_down),
    (1 * math.cos(math.radians(345)), 1 * math.sin(math.radians(345)) - 0.5, pen_down),
    (1 * math.cos(math.radians(330)), 1 * math.sin(math.radians(330)) - 0.5, pen_down),
    (1 * math.cos(math.radians(315)), 1 * math.sin(math.radians(315)) - 0.5, pen_down),
    (1 * math.cos(math.radians(285)), 1 * math.sin(math.radians(285)) - 0.5, pen_down),
    (1 * math.cos(math.radians(270)), 1 * math.sin(math.radians(270)) - 0.5, pen_down),
    (1 * math.cos(math.radians(255)), 1 * math.sin(math.radians(255)) - 0.5, pen_down),
    (1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240)) - 0.5, pen_down),
    (1 * math.cos(math.radians(225)), 1 * math.sin(math.radians(225)) - 0.5, pen_down),
    (1 * math.cos(math.radians(210)), 1 * math.sin(math.radians(210)) - 0.5, pen_down),
    (1 * math.cos(math.radians(195)), 1 * math.sin(math.radians(195)) - 0.5, pen_down),
]

t_values = [
    (-1, 1, pen_down),
    (1, 1, pen_down),
    (1, 1, pen_up),
    (0, 1, pen_up),
    (0, 1, pen_down),
    (0, -1, pen_down)
]

u_values = [
    (-1, 1, pen_down),
    (1 * math.cos(math.radians(180)), 1 * math.sin(math.radians(180)), pen_down),
    (1 * math.cos(math.radians(195)), 1 * math.sin(math.radians(195)), pen_down),
    (1 * math.cos(math.radians(210)), 1 * math.sin(math.radians(210)), pen_down),
    (1 * math.cos(math.radians(225)), 1 * math.sin(math.radians(225)), pen_down),
    (1 * math.cos(math.radians(240)), 1 * math.sin(math.radians(240)), pen_down),
    (1 * math.cos(math.radians(255)), 1 * math.sin(math.radians(255)), pen_down),
    (1 * math.cos(math.radians(270)), 1 * math.sin(math.radians(270)), pen_down),
    (1 * math.cos(math.radians(285)), 1 * math.sin(math.radians(285)), pen_down),
    (1 * math.cos(math.radians(315)), 1 * math.sin(math.radians(315)), pen_down),
    (1 * math.cos(math.radians(330)), 1 * math.sin(math.radians(330)), pen_down),
    (1 * math.cos(math.radians(345)), 1 * math.sin(math.radians(345)), pen_down),
    (1 * math.cos(math.radians(360)), 1 * math.sin(math.radians(360)), pen_down),
    (1, 1, pen_down)
]

v_values = [
    (-1, 1, pen_down),
    (0, -1, pen_down),
    (1, 1, pen_down)
]

w_values = [
    (-2, 1, pen_down),
    (-1, -1, pen_down),
    (0, 1, pen_down),
    (1, -1, pen_down),
    (2, 1, pen_down)
]

x_values = [
    (-1, 1, pen_down),
    (1, -1, pen_down),
    (1, -1, pen_up),
    (1, 1, pen_up),
    (1, 1, pen_down),
    (-1, -1, pen_down)
]

y_values = [
    (-1, 1, pen_down),
    (0, 0, pen_down),
    (1, 1, pen_down),
    (1, 1, pen_up),
    (0, 0, pen_up),
    (0, 0, pen_down),
    (0, -1, pen_down)
]

z_values = [
    (-1, 1, pen_down),
    (1, 1, pen_down),
    (-1, -1, pen_down),
    (1, -1, pen_down)
]



letter_equivalent_values = {
    "A": a_values,
    "B": b_values,
    "C": c_values,
    "D": d_values,
    "E": e_values,
    "F": f_values,
    "G": g_values,
    "H": h_values,
    "I": i_values,
    "J": j_values,
    "K": k_values,
    "L": l_values,
    "M": m_values,
    "N": n_values,
    "O": o_values,
    "P": p_values,
    "Q": q_values,
    "R": r_values,
    "S": s_values,
    "T": t_values,
    "U": u_values,
    "V": v_values,
    "W": w_values,
    "X": x_values,
    "Y": y_values,
    "Z": z_values
}
