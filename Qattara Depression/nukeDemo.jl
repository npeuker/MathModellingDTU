using GLPK, Cbc, JuMP, SparseArrays
using DataFrames, CSV

# read elevation_interpolated.csv file
height_interpolated = CSV.File("elevation_interpolated.csv")
#convert height_interpolated into same format as H 
height = []
for row in height_interpolated
    push!(height, row[1])
end
height = Int.(height)

H = [
10
30
70
50
70
120
140
120
100
80
]

K = [
300 140 40
]

function constructA(H,K)
    # Make a function that returns A when given H and K
    h = length(H)
    A = zeros(h,h)
    for i=1:h
        for j=1:h
            if i==j
                A[i,j] = 300
            elseif i==j+1 
                A[i,j] = 140
            elseif i==j+2
                A[i,j] = 40
            elseif i==j-1
                A[i,j] = 140
            elseif i==j-2
                A[i,j] = 40
            end
        end
    end
    return A
end

# A should be structured as follows
A = [300.0  140.0   40.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
     140.0  300.0  140.0   40.0    0.0    0.0    0.0    0.0    0.0    0.0
      40.0  140.0  300.0  140.0   40.0    0.0    0.0    0.0    0.0    0.0
       0.0   40.0  140.0  300.0  140.0   40.0    0.0    0.0    0.0    0.0
       0.0    0.0   40.0  140.0  300.0  140.0   40.0    0.0    0.0    0.0
       0.0    0.0    0.0   40.0  140.0  300.0  140.0   40.0    0.0    0.0
       0.0    0.0    0.0    0.0   40.0  140.0  300.0  140.0   40.0    0.0
       0.0    0.0    0.0    0.0    0.0   40.0  140.0  300.0  140.0   40.0
       0.0    0.0    0.0    0.0    0.0    0.0   40.0  140.0  300.0  140.0
       0.0    0.0    0.0    0.0    0.0    0.0    0.0   40.0  140.0  300.0
]



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

myModel, x,R = solveIP(height,K)
println("Type of myModel", typeof(myModel))

# save myModel, x and R to a csv file in folder
df = DataFrame(myModel=myModel, x=x, R=R)
CSV.write("nukeDemo.csv", df)


