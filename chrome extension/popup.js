document.addEventListener('DOMContentLoaded', function () {
  // Get the current tab URL
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];
    const curr_url = currentTab.url;

    // Get the tab ID
    const tabId = currentTab.id;

    // Specify the script to inject
    const scriptToInject = {
      target: { tabId: tabId },
      function: (data) => {
        return document.body.innerText.slice(0, 80);
      },
    };

    // Inject the script using chrome.scripting.executeScript
    chrome.scripting
      .executeScript(scriptToInject)
      .then((results) => {
        // Extracted text content from the script execution results
        const bodyText = results[0] || '';
        // console.log(bodyText)

        // JSON data containing 'url' and 'context'
        const dataToSend = {
          url: curr_url,
          context: bodyText,
        };


        // Make a request to your Python API
        fetch('http://127.0.0.1:5000/api/spooftest', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(dataToSend), // Include the data object
        })
          .then((response) => response.json())
          .then((data) => {
            // Update the popup with the API response
            const resBox = document.getElementById('result')
            if (data.message == "SAFE"){
              resBox.classList.add('safebox')
              resBox.textContent = "Website Looks Safe!";
            }
            else if (data.message == "UNSAFE") {
              resBox.classList.add('unsafebox')
              resBox.textContent = "Careful! Site seems Fake";
            }
            else {
              resBox.textContent = data.message;
            }


          })
          .catch((error) => {
            console.error('Error:', error);
          });
      })
      .catch((error) => {
        console.error('Error injecting script:', error);
      });
  });
});
