keys = [];
for (let i = 0; i < 26; i++) {
    keys.push(i);
}
const wordToBreak = prompt("YO");
const arr = wordToBreak.split("");
const finalArray = [];
keys.map((key) => {
    let newArr = [];
    let char = "";
    arr.map((character) => {
        if (character.charCodeAt(0) + key > 90) {
            char = 65 + (character.charCodeAt(0) + key - 91);
        }
        else {
            char = character.charCodeAt(0) + key; 
        }

        newArr.push(String.fromCharCode(char));
    })
    newArr = newArr.join(" ")
    finalArray.push(newArr);
})


console.log(finalArray);
