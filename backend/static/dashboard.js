fetch('/zones')  // or '/trips' depending on your route
  .then(response => response.json())
  .then(data => {
      console.log(data); 
     
  });
