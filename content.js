
var x = window.location.href
x=x.substring(x.indexOf("=")+1);
//alert(x)

console.log(x);
fetch('http://127.0.0.1:5000/summarize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ video_id: x }),
})
.then(response => response.text())
.then(data => {
    console.log(data)
    alert(data)
   // console.log('Summary from server:', data.summary);
})
.catch(error => {
    console.error('Error:', error);
});

//alert("done")
