todo = function() {
    fetch('/my/request', {
        method: 'POST',
        body: JSON.stringify({
          'description': 'some description here'
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      });
}()
