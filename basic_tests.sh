#!/bin/bash
dataset=(Clicks_50k Toys_and_Games Beauty Sports_and_Outdoors Home Yelp)

cd SASRec/src

for((i=0; i<"${#dataset[@]}";i++)); do
    for j in {0..2}; do
        python3 main.py --data_name="${dataset[$i]}" --aug_type="$j" --model_idx="$((i * 10 + j))"
    done
done

cd GRU4Rec/src

for((i=0; i<"${#dataset[@]}";i++)); do
    for j in {0..2}; do
        python3 main.py --data_name="${dataset[$i]}" --aug_type="$j" --model_idx="$((i * 10 + j))"
    done
done

cd ..
cd ..