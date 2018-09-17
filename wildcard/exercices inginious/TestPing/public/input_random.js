// Retrieve random inputs
// The second argument is the base of the number the 'radix'
var a = parseInt(input["@random"][0] * 5000 + 10000); 

// Retrieve HTML tag we placed in the statement
// and replace them by the generated random value
document.getElementById("ipr1").innerHTML = a.toString();//16);
