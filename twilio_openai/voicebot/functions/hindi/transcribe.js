exports.handler = function (context, event, callback) {
  const twiml = new Twilio.twiml.VoiceResponse();
  // const recordingSid = event.RecordingSid;
  // const transcriptionSid = event.TranscriptionSid;
  // console.log(`Recording SID: ${recordingSid}`);
  // console.log(`Transcription SID: ${transcriptionSid}`);
  const fs = require('fs');
  const config = JSON.parse(fs.readFileSync('config.json', 'utf-8'));
  const Voice_assistant = config.languages.hindi.voice;

    // Handle the rest of the conversation logic here
    if (!event.request.cookies.convo) {
      // Greet the user at the beginning of the conversation
      twiml.say(
        {
          // voice: 'Polly.Joanna-Neural',
          voice :Voice_assistant,
        },
        config.languages.hindi.welcome_msg
      );
    }
    // Listen to the user's speech and pass the input to the /respond Function
    twiml.gather({
      action: '/hindi/respond',// Send the collected input to /respond
      speechTimeout: 3, // Automatically determine the end of user speech
      speechModel: 'phone-call', // Use the conversation-based speech recognition model
      input: 'speech dtmf', // Specify speech as the input type
       numdigits:1,
    });
  

  // Create a Twilio Response object
  const response = new Twilio.Response();
  console.log(response)

  // Set the response content type to XML (TwiML)
  response.appendHeader('Content-Type', 'application/xml');

  // Set the response body to the generated TwiML
  response.setBody(twiml.toString());

  // If no conversation cookie is present, set an empty conversation cookie
  if (!event.request.cookies.convo) {
    response.setCookie('convo', '', ['Path=/']);
  }

  // Return the response to Twilio
  return callback(null, response);
};
