#!/bin/bash

echo "hello world!"
<< comment
comment start
this is comment block
comment end
comment
function function_name(){
name="paras"
echo "function argument :- $#"
echo "my name is $name"

echo "current time $(date)"

echo "what is your name..."

read username

echo "your enter name :-"$username
echo "YOUR 1ST ARGUMENT IS :- " $0
echo "your 1st argument :-"$1
echo "your 2nd argument :-"$2

if [[ $username == "paras" ]];
then
        echo "This is your PC"
elif [[ $username == "hello" ]];
then
        echo "This is Your PC" $username
else
        echo "Wrong User Call"
fi

for (( i=0; i<=10; i++ ))
do
        echo "forloop run $i this time"
done

num=0

while [[ $num -le 5 ]]
do
        echo "this is while_loop $num position"
        num=$((num+1))
done

}

function_name $1 $2 $3
