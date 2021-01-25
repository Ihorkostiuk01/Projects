#*******************************************
# Pakiety matematyczne
# Project: Maze runner
# Ihor Kostiuk(255915)
# Module to solve the maze
#*******************************************
module Maze_solver
    export solve_image

    include("./generator.jl")
    using .Maze_generator

    using Images

    function way_finder(matrix, p, height, weight)
        """
        Function to find the next point to pass
        Args:
        -matrix - maze matrix;
        -p - point
        -heigh - heigh of maze
        -heigh - weigh of maze
        """
        neighbours = [Point(p.x, p.y+1), # up
                    Point(p.x, p.y-1), #down
                    Point(p.x-1, p.y), #left
                    Point(p.x+1, p.y)] #right
        aim = [] #list of points
        for i in neighbours 
            if 0<i.x<=height && 0<i.y<=weight && matrix[i.x,i.y]==1 #If the current point has unvisited "neighbors"
                push!(aim, i) #Push the current point into the stack
            end
        end
        if length(aim)!= 0 #if list si not empty
            rand(aim)      #select a random point from the list
        else
            Point(0,0)     #return to the starting point
        end
    end

    function solve_matrix(img)
        """
        Function to drawing a route of the maze.
        Args:
        -img - image of the maze
         Returns:
        - The matrix of the labyrinth with its passage
        """
        matrix = Float64.(channelview(img)) #converting an image into a matrix
        height, weight = size(matrix) #height and weight of the matrix
        p = Point(1,2) #start
        exit = Point(height-1,weight) #exit
        matrix[exit.x,exit.y] = 1
        container = [] #list of points
        push!(container, p) #adding the starting point to the list
        while p.x != exit.x || p.y != exit.y # till exit is not founded
            matrix[p.x,p.y] = 0.4  #color = grey
            np = way_finder(matrix, p, height, weight) 
            if np.x == np.y == 0 #not correct path
                matrix[p.x,p.y] = 0.99 #color = white
                p = pop!(container) #turn back to the last element of the list
            else
                push!(container, p) #adding point to the list
                p = np
            end
        end
        return matrix
    end

    function solve_image(matrix)
        """
        Function to save the image of solved maze
        Args:
        -matrix - matrix of solved maze
        """
        maze = solve_matrix(matrix)
        height,weight = size(maze) #height and weight of maze
        maze[height-1,weight] = 0.4 #color of the end point = gray
        img = Gray.(maze) #converting matrix ti the image
        Images.save("Solve.png", img) #saving the image
    end
end