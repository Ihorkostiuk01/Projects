#*******************************************
# Pakiety matematyczne
# Project: Maze runner
# Roman Furman(255909)
# Module to create maze
#*******************************************
module Maze_generator
    export Point, maze_image

    using Images

    mutable struct Point
        x::Int64 # vertical
        y::Int64 # horisont
        Point(x, y) = new(x, y)
    end

    function points_around(matrix, p, height, weight)
        """Function finds unvisited points around.
            Arguments:
                matrix(Array{Int64,2}): maze matrix.
                p(Point): looking for neighbors around this point.
                height(Int64): maximum matrix height.
                weight(Int64): maximum matrix width.

        """
        neighbours = [Point(p.x, p.y+2), # up
                    Point(p.x, p.y-2), # down
                    Point(p.x-2, p.y), # left
                    Point(p.x+2, p.y)] # right
        aim = [] #array with neighbours points
        for i in neighbours
            if 0<i.x<=height && 0<i.y<=weight && matrix[i.x,i.y] == 2 #looking for a neighbors
                push!(aim, i) #add the found neighbor to the array
            end
        end
        if length(aim) != 0 #if the array is not empty
            rand(aim) #take a random neighbor
        else 
            Point(-1,-1) #mark a dead end
        end
    end

    function barrier_breaker(matrix, newp, oldp)
        """Аunction paves the way between the new and the old point.
            Arguments:
                matrix(Array{Int64,2}): maze matrix.
                newp(Point): new point.
                oldp(Point): old point.
        """
        x = (oldp.x + newp.x) ÷ 2 #take the average coordinate of x
        y = (oldp.y + newp.y) ÷ 2 #take the average coordinate of y
        matrix[x,y] = 1 #call the new point as a way
    end

    function matrix_generator(height, weight)
        """Function generates a matrix of ones and zeros in the form of a maze.
            Arguments:
                height(Int64): matrix height.
                weight(Int64): matrix width.
            Return:
                matrix(Array{Int64,2}): matrix of ones and zeros forming a maze.
        
        """
        matrix = [ 2(i&j&1) for i in 0:height, j in 0:weight ] #generate start matrix
        p = Point(2,2) #starting point
        container = [] #create empty array
        push!(container, p) #add first point to array
        while length(container) != 0 #until the stack is empty
            matrix[p.x,p.y] = 1 #mark white that point that we visited
            newp = points_around(matrix, p, height, weight) #take new point
            #if there are no neighbors - go back
            if newp.x == newp.y == -1 #check if this is a dead end
                p = pop!(container) #pick up the last item in array
            else
                push!(container, p) #add a new point in array
                barrier_breaker(matrix, newp, p) #call the gap between the new and the old point our way
                p = newp #determined new point as old
            end
        end
        matrix[1,2] = 1 #entrance to the maze
        matrix[height,weight+1] = 1 #exit from the maze
        return matrix
    end

    function maze_image(height, weight)
        """Function saves the maze visualization in .png format.
            Arguments:
                height(Int64): matrix height.
                weight(Int64): matrix width.

        """
        maze = matrix_generator(height, weight) #generate a matrix(maze)
        picture = Gray.(maze) #render the matrix into a picture
        Images.save("Maze.png", picture) #save our picture into .png file 
    end

end
