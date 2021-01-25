#*******************************************
# Pakiety matematyczne
# Project: Maze runner
# Roman Furman(255909), Ihor Kostiuk(255915)
# Visualization in GUI
#*******************************************
include("./generator.jl")
include("./solver.jl")
using .Maze_generator, .Maze_solver
using Images
using Gtk, ImageView, TestImages

win = GtkWindow("Maze Generator",600,600)

general_box = GtkBox(:v)

str_box = GtkBox(:v)

tittle = GtkLabel("Maze Generator")
GAccessor.markup(tittle, """<b>Maze Generator</b>""")
push!(str_box,tittle)

label = GtkLabel("Heigh:")
push!(str_box,label)

height = GtkComboBoxText()
choices = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
for choice in choices
  push!(height,choice)
end
set_gtk_property!(height, :active, 4)
push!(str_box, height)

label = GtkLabel("Width:")
push!(str_box, label)

weight = GtkComboBoxText()
choices2 = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
for choice in choices2
  push!(weight, choice)
end
set_gtk_property!(weight, :active,4)
push!(str_box, weight)


buttom_box = GtkBox(:h)

b_generate = GtkButton("Generate")
push!(buttom_box, b_generate)

function buttom_generate()
  """Function for a button that shows the generated maze image.
  """
  maze_image(parse(Int64, Gtk.bytestring(GAccessor.active_text(height))), parse(Int64, Gtk.bytestring(GAccessor.active_text(height))))
  image = load("/Users/romafurman/Semester2/Pakietymatemat/Maze/Maze.png")
  imshow(c, image)
  print("Maze created")
end

signal_connect(buttom_generate, b_generate, :clicked)


b_solve = GtkButton("Solve")
push!(buttom_box, b_solve)

function buttom_solve()
  """Function for a button that shows the solved maze image.
  """
    maze = load("/Users/romafurman/Semester2/Pakietymatemat/Maze/Maze.png")
    solve_image(maze)
    image = load("/Users/romafurman/Semester2/Pakietymatemat/Maze/Solve.png")
    imshow(c, image)
    print("Maze solved")
end

signal_connect(buttom_solve, b_solve, "clicked")


b_close = GtkButton("Close")
push!(buttom_box, b_close)
signal_connect(b_close, :clicked) do widget
  Gtk.destroy(win)
  println("Exit")
end

set_gtk_property!(buttom_box, :spacing, 200)


push!(general_box, str_box)
push!(general_box, buttom_box)

frame, c = ImageView.frame_canvas(:auto)
push!(general_box, frame)

push!(win, general_box)
showall(win)