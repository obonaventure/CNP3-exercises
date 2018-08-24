
// This Javascript file is used to reflect the shuffled network in the frontend.
// It will be replaced by a proper graphic library.

function random(i, n) {
    return parseInt(input["@random"][i] * n);
}

function shuffle(list_to_shuffle) {
    var n = list_to_shuffle.length;
    while (n > 0) {
        var index = random(n-1, n);
        n = n-1;
        var temp = list_to_shuffle[n];
        list_to_shuffle[n] = list_to_shuffle[index];
        list_to_shuffle[index] = temp;
    }
}

ases = ["as1", "as2", "as3", "as4", "as5"]
shuffle(ases)

document.getElementById("as1").innerHTML = ases[0];
document.getElementById("as2").innerHTML = ases[1];
document.getElementById("as3").innerHTML = ases[2];
document.getElementById("as4").innerHTML = ases[3];
document.getElementById("as5").innerHTML = ases[4];
