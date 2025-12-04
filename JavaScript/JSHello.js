console.log("Hello, Students of LSS HIGH, Class 12")

// document.write("Welcome to JavaScript Programming!") // will show that write method is deprecated now

console.log("Welcome to JavaScript Programming!");

const newPar = document.createElement("p"); // Create a new paragraph element

newPar.textContent = "This is the content loaded from the js code of another files."; // Set its text content

document.body.appendChild(newPar); 
/* Append the new paragraph to the body of the document

appendChild is the modern way to add elements to the DOM. It means "append a child element to a parent element."

The dot notation (.) is used to access properties and methods of objects in JavaScript.
Here, 
document is an object representing the web page, 
body is a property of the document object representing the body section of the HTML, 
and 
appendChild is a method that adds a new child element to that body.

*/
