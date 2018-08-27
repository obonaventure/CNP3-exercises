
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

ases = [{"asn":"as1", "prefix":"1111::/48"}, 
        {"asn":"as2", "prefix":"2222::/48"}, 
        {"asn":"as3", "prefix":"3333::/48"}, 
        {"asn":"as4", "prefix":"4444::/48"}, 
        {"asn":"as5", "prefix":"5555::/48"}]
shuffle(ases)

document.getElementsByName("as1").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[0].asn;
});
document.getElementsByName("as2").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[1].asn;
});
document.getElementsByName("as3").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[2].asn;
});
document.getElementsByName("as4").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[3].asn;
});
document.getElementsByName("as5").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[4].asn;
});

document.getElementsByName("as1_prefix").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[0].prefix;
});
document.getElementsByName("as2_prefix").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[1].prefix;
});
document.getElementsByName("as3_prefix").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[2].prefix;
});
document.getElementsByName("as4_prefix").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[3].prefix;
});
document.getElementsByName("as5_prefix").forEach(function(v, i, arr) {
  arr[i].innerHTML = ases[4].prefix;
});
