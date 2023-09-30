// Import the necessary modules
const twilio = require('twilio');
const express = require('express');
const path = require('path');

// Initialize Express.js
const app = express();
const port = process.env.PORT || 3000;

// Serve the HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Twilio Account SID and Auth Token
const accountSid = process.env.ACCOUNT_SID;
const authToken = process.env.AUTH_TOKEN;
const client = require('twilio')(accountSid, authToken);
const Twilio_number = process.env.TWILIO_NUMBER

// Fetch call logs and send them as JSON
app.get('/api/calls', (req, res) => {
    client.calls.list({from:Twilio_number, limit: 1})
        .then((calls) => {
            res.json(calls);
        })
        .catch((error) => {
            console.error('Error fetching call logs:', error);
            res.status(500).json({ error: 'Error fetching call logs' });
        });
});

client.recordings
  .list({ limit: 1 }) // You can adjust the limit as needed
  .then((recordings) => {
    recordings.forEach((recording) => {
      console.log(`Recording SID: ${recording.sid}`);
      console.log(`Call SID: ${recording.callSid}`);
      console.log(`Recording URL: ${recording.uri}`);
      console.log('-----');
    });
  })
  .catch((error) => {
    console.error('Error fetching recordings:', error);
  });

// Start the Express.js server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
