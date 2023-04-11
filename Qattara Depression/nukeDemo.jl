using GLPK, Cbc, JuMP, SparseArrays
using DataFrames, CSV

# reading elevation_interpolated.csv
height_interpolated = CSV.File("elevation_interpolated.csv")
height = []

println("Read csv file")

# converting it into the right format
for row in height_interpolated
    push!(height, row[1])
end
height = Int.(height)

# values of K for different types of nukes
K = [
300 140 40
]

K0 = [
300 140 40
]

K1 = [
500 230 60
]

K2 = [
1000 400 70
]

# constructing the matrix A when H and K are given
function constructA(H,K)
    h = length(H)
    A = zeros(h,h)
    for i=1:h
        for j=1:h
            if i==j
                A[i,j] = K[1,1]
            elseif i==j+1 || i==j-1
                A[i,j] = K[1,2]
            elseif i==j+2 || i==j-2
                A[i,j] = K[1,3]
            end
        end
    end
    return A
end

function solveIP(H, K)
    h = length(H)
    myModel = Model(Cbc.Optimizer)
    # If your want ot use GLPK instead use:
    # myModel = Model(GLPK.Optimizer)

    A = constructA(H,K)

    @variable(myModel, x[1:h], Bin )
    @variable(myModel, R[1:h] >= 0 )

    @objective(myModel, Min, sum(x[j] for j=1:h) )

    @constraint(myModel, [j=1:h],R[j] >= H[j] + 10 )
    @constraint(myModel, [i=1:h],R[i] == sum(A[i,j]*x[j] for j=1:h) )
    optimize!(myModel)

    if termination_status(myModel) == MOI.OPTIMAL
        # println("Objective value: ", JuMP.objective_value(myModel))
        # println("x = ", JuMP.value.(x))
        # println("R = ", JuMP.value.(R))
    else
        println("Optimize was not succesful. Return code: ", termination_status(myModel))
    end
    return  JuMP.objective_value(myModel),JuMP.value.(x), JuMP.value.(R)
end

# myModel, x,R = solveIP(height,K)
# println("Type of myModel", typeof(myModel))

# save myModel, x and R to a csv file in folder
# df = DataFrame(myModel=myModel, x=x, R=R)
# CSV.write("nukeDemo.csv", df)

function newSolveIP(H,K)
    h = length(H)
    myModel = Model(Cbc.Optimizer)
    # If your want ot use GLPK instead use:
    # myModel = Model(GLPK.Optimizer)

    A = constructA(H,K)

    @variable(myModel, x[1:h], Bin )
    @variable(myModel, R[1:h] >= 0 )

    @variable(myModel, t[1:h] >= 0)
    @constraint(myModel, [j=1:h], R[j] - H[j] - 10 <= t[j])
    @constraint(myModel, [j=1:h], -R[j] + H[j] + 10 <= t[j])
    @objective(myModel, Min, sum(t[j] for j=1:h))
    @objective(myModel, Min, sum(x[j] for j=1:h) )

    @constraint(myModel, [j=1:h],R[j] >= H[j] + 10 )
    @constraint(myModel, [i=1:h],R[i] == sum(A[i,j]*x[j] for j=1:h) )
    optimize!(myModel)

    if termination_status(myModel) == MOI.OPTIMAL
        # println("Objective value: ", JuMP.objective_value(myModel))
        # println("x = ", JuMP.value.(x))
        # println("R = ", JuMP.value.(R))
    else
        println("Optimize was not succesful. Return code: ", termination_status(myModel))
    end
    return  JuMP.objective_value(myModel),JuMP.value.(x), JuMP.value.(R)
end

# myNewModel, newx,newR = newSolveIP(height,K)
# df = DataFrame(myNewModel=myNewModel, newx=newx, newR=newR)
# CSV.write("newNukeDemo.csv", df)

function solveIP5(H,K)
    h = length(H)
    myModel = Model(Cbc.Optimizer)
    # If your want ot use GLPK instead use:
    # myModel = Model(GLPK.Optimizer)

    A = constructA(H,K)

    @variable(myModel, x[1:h], Bin )
    @variable(myModel, R[1:h] >= 0 )

    @variable(myModel, t[1:h] >= 0)
    @constraint(myModel, [j=1:h], R[j] - H[j] - 10 <= t[j])
    @constraint(myModel, [j=1:h], -R[j] + H[j] + 10 <= t[j])
    @objective(myModel, Min, sum(t[j] for j=1:h))
    @objective(myModel, Min, sum(x[j] for j=1:h) )

    # make sure that two x values next to each other is not both 1

    @constraint(myModel, [j=2:h-1], x[j-1] + x[j] <= 1)
    @constraint(myModel, [j=2:h-1], x[j] + x[j+1] <= 1 )
    @constraint(myModel, [j=1:h],R[j] >= H[j] + 10 )
    @constraint(myModel, [i=1:h],R[i] == sum(A[i,j]*x[j] for j=1:h) )
    optimize!(myModel)

    if termination_status(myModel) == MOI.OPTIMAL
        # println("Objective value: ", JuMP.objective_value(myModel))
        # println("x = ", JuMP.value.(x))
        # println("R = ", JuMP.value.(R))
    else
        println("Optimize was not succesful. Return code: ", termination_status(myModel))
    end
    return  JuMP.objective_value(myModel),JuMP.value.(x), JuMP.value.(R)
end

# myModel5, x5,R5 = solveIP5(height,K)
# df = DataFrame(myModel5=myModel5, x5=x5, R5=R5)
# CSV.write("nukeDemo5.csv", df)

function solveIP6(H,K)
    h = length(H)
    myModel = Model(Cbc.Optimizer)
    # If your want ot use GLPK instead use:
    #myModel = Model(GLPK.Optimizer)

    A0 = constructA(H,K0)
    A1 = constructA(H,K1)
    A2 = constructA(H,K2)
    

    @variable(myModel, x[1:h], Bin )
    @variable(myModel, R[1:h] >= 0 )
    @variable(myModel, t[1:h] >= 0)
    @variable(myModel, y0, Bin)
    @variable(myModel, y1, Bin)
    @variable(myModel, y2, Bin)

    # @constraint(myModel, [j=1:h], R[j] - H[j] - 10 <= t[j])
    # @constraint(myModel, [j=1:h], -R[j] + H[j] + 10 <= t[j])

    # implement the possibility of using different yields from settings

    # @objective(myModel, Min, sum(t[j] for j=1:h))
    # @objective(myModel, Min, sum(x[j] for j=1:h) )

    @objective(myModel, Min, sum(R[j]-H[j]-10 for j=1:h) )

    # make sure that two x values next to each other is not both 1

    @constraint(myModel, [j=2:h-1], x[j-1] + x[j] <= 1)
    @constraint(myModel, [j=2:h-1], x[j] + x[j+1] <= 1 )
    @constraint(myModel, [j=1:h],R[j] >= H[j] + 10 )
    # @constraint(myModel, [i=1:h],R[i] == sum(A[i,j]*x[j] for j=1:h) )
    @constraint(myModel, [i=1:h],R[i] == y0*sum(A0[i,j]*x[j] for j=1:h) + y1*sum(A1[i,j]*x[j] for j=1:h) + y2*sum(A2[i,j]*x[j] for j=1:h))
    @constraint(myModel, y0 + y1 + y2 == 1)

    optimize!(myModel)

    if termination_status(myModel) == MOI.OPTIMAL
        # println("Objective value: ", JuMP.objective_value(myModel))
        # println("x = ", JuMP.value.(x))
        # println("R = ", JuMP.value.(R))
    else
        println("Optimize was not succesful. Return code: ", termination_status(myModel))
    end
    return  JuMP.objective_value(myModel),JuMP.value.(x), JuMP.value.(R)
end

#myModel6, x6,R6 = solveIP6(height, K2)
#df = DataFrame(myModel6=myModel6, x6=x6, R6=R6)
#CSV.write("nukeDemo6.csv", df)






###################################################################################

function solveIP(H, K0, K1, k2)
    h = length(H)
    myModel = Model(Cbc.Optimizer)
    # If your want ot use GLPK instead use:
    # myModel = Model(GLPK.Optimizer)

    A0 = constructA(H,K0)
    A1 = constructA(H,K1)
    A2 = constructA(H,K2)

    @variable(myModel, x[1:h], Bin )
    @variable(myModel, R[1:h] >= 0 )

    @objective(myModel, Min, sum(x[j] for j=1:h) )

    @constraint(myModel, [j=1:h],R[j] >= H[j] + 10 )
    @constraint(myModel, [i=1:h],R[i] == sum(A1[i,j]*x[j] for j=1:h) )
    optimize!(myModel)

    if termination_status(myModel) == MOI.OPTIMAL
        # println("Objective value: ", JuMP.objective_value(myModel))
        # println("x = ", JuMP.value.(x))
        # println("R = ", JuMP.value.(R))
    else
        println("Optimize was not succesful. Return code: ", termination_status(myModel))
    end
    return  JuMP.objective_value(myModel),JuMP.value.(x), JuMP.value.(R)
end

 myModel, x,R = solveIP(height,K0, K1, K2)
 println("Type of myModel", typeof(myModel))

# save myModel, x and R to a csv file in folder
 df = DataFrame(myModel=myModel, x=x, R=R)
 CSV.write("nukeDemotest.csv", df)