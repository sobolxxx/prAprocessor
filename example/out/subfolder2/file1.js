
// Random number generator between 1 and 100
function getRandomNumber() {
  return Math.floor(Math.random() * 100) + 1;
}

// Random greeting generator
function getRandomGreeting() {
  const greetings = ["Hello", "Hi", "Hey", "Howdy", "Hola", "Bonjour"];
  return greetings[Math.floor(Math.random() * greetings.length)];
}

// Concatenate greeting and number
function createMessage() {
  const randomGreeting = getRandomGreeting();
  const randomNumber = getRandomNumber();
  return `${randomGreeting}, your random number is ${randomNumber}!`;
}

// Log message to console
function logMessage() {
  const message = createMessage();
  console.log(message);
}

// Call logMessage every 3 seconds
setInterval(logMessage, 3000);

