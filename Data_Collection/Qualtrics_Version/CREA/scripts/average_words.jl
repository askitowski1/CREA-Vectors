using CSV,DataFrames,Statistics,BSON

crea_attributenames = ["Vision", "Bright", "Dark", "Color", "Pattern", "Large", "Small", "Motion", "Biomotion", "Fast", "Slow", "Shape", "Complexity", "Face", "Body", "Touch", "Pain", "Audition", "Loud", "Low", "High", "Sound", "Music", "Speech", "Taste", "Smell", "Head", "UpperLimb", "LowerLimb", "Manipulation", "Landmark", "Path", "Scene", "Near", "Toward", "Away", "Number", "Time", "Duration", "Long", "Short", "Caused", "Consequential", "Social", "Human", "Communication", "Self", "Cognition", "Benefit", "Harm", "Pleasant", "Unpleasant", "Happy", "Sad", "Angry", "Disgusted", "Fearful", "Surprised", "Drive", "Needs", "Attention", "Arousal", "Temperature", "Texture", "Weight"]
combined_attributes = Dict(
    "Temperature" => ["Hot","Cold"],
    "Texture" => ["Smooth","Rough"],
    "Weight" => ["Heavy","Light"]
)

# Make sure the CREA vector is in the correct order and columns are averaged properly
function get_creavec(df::DataFrame,rownum::Vector{Int})
    vec = Float64[]
    for n in crea_attributenames
        if n in names(df)
            push!(vec,mean(df[rownum,n]))
        elseif n in keys(combined_attributes)
            subvec = Float64[]
            for nn in combined_attributes[n]
                if nn in names(df)
                    append!(subvec,df[rownum,nn])
                else
                    error("Could not find column $n, or its component $nn")
                end
            end
            push!(vec,mean(subvec))
        else
            error("Could not find column $n")
        end
    end
    
    return vec
end             

get_creavec(df::DataFrame,rownum::Int) = get_creavec(df,[rownum])

dist(df::DataFrame,i::Int,j::Vector{T}) where T<:Real = cor(get_creavec(df,i),j)

function get_bestvec(df::DataFrame,wordii::Vector{Int};close_thresh=0.3)
    best = (-Inf,)
    for i in wordii
        for j in wordii
            i==j && continue
            x = dist(df,i,get_creavec(df,j))
            x > best[1] && (best = (x,i,j))
        end
    end

    best[1] < close_thresh && error("best = $best !!!")

    used_i = [best[2],best[3]]
    bestvec = get_creavec(df,used_i)

    while length(used_i) < length(wordii)
        best = (-Inf,)
        for i in wordii
            i in used_i && continue
            x = dist(df,i,bestvec)
            x > best[1] && (best = (x,i))
        end
        if best[1]>close_thresh
            push!(used_i,best[2])
            bestvec = get_creavec(df,used_i)
        else
            break
        end
    end

    (;bestvec,used_i)
end

function get_bestvec(df::DataFrame,word::AbstractString;catch_acc_min=0.8,args...)
    wordii = findall((df[!,:Word].==word) .* (df[!,:CatchAcc] .>= catch_acc_min))
    get_bestvec(df,wordii;args...)
end


# Function to parse a series of words collected from the new Qualtrics version
function parse_newwords(fname::String)
    df = CSV.read(fname,DataFrame)

    all_words = unique(df[!,:Word])

    crea_vecs = Dict{String,Vector{Float64}}()

    for w in all_words
        crea_vecs[w] = get_bestvec(df,w).bestvec
    end

    return crea_vecs
end

# Function to collect vectors from already processed words
function parse_processedwords(fname::String)
    df = CSV.read(fname,DataFrame)
    crea_vecs = Dict{String,Vector{Float64}}()

    for i in 1:size(df,1)
        w = df[i,:Word]
        sum(df[!,:Word] .== w) != 1 && error("Multiple entries found for word $w !")
            
        crea_vecs[w] = get_creavec(df,i)
    end

    return crea_vecs
end

# Collect vectors and update the BSON file
function parse_newwords(fname::String,bson_fname::String;overwrite::Bool=false)
    db = isfile(bson_fname) ? BSON.load(bson_fname) : Dict{String,Vector{Float64}}()

    new_db = parse_newwords(fname)

    for w in keys(new_db)
        if overwrite==true || !(haskey(db,w))
            db[w] = new_db[w]
        end
    end

    BSON.bson(bson_fname,db)
end

# Collect vectors and update the BSON file
function parse_processedwords(fname::String,bson_fname::String;overwrite::Bool=false)
    db = isfile(bson_fname) ? BSON.load(bson_fname) : Dict{String,Vector{Float64}}()

    new_db = parse_processedwords(fname)

    for w in keys(new_db)
        if overwrite==true || !(haskey(db,w))
            db[w] = new_db[w]
        end
    end

    BSON.bson(bson_fname,db)
end