exports.handler = function (context, event, callback) {
    const twiml = new Twilio.twiml.VoiceResponse();
    const userSpeech = event.SpeechResult || '';
  
    // Check if the user has pressed "1" during the call
    if (userSpeech === '1') {
      // If "1" is pressed, initiate a call to another number
      gather.say('The call is routed to manual agent');
      twiml.dial({
        callerId: process.env.FROM_TWILIO_NUMBER, // Your Twilio phone number
      }, process.env.TARGET_PHONE_NUMBER); // Replace with the number you want to call
    //   gather.say('The call is routed to manual agent');
    } else {
      // Handle the rest of the conversation logic here
      if (!event.request.cookies.convo) {
        // Greet the user at the beginning of the conversation
        twiml.say(
          {
            // voice: 'Polly.Joanna-Neural',
            voice :'Polly.Kajal-Neural',
          },
          // "Hey! I'm Joanna, a chatbot created using Twilio and ChatGPT. What would you like to talk about today?"
          "अरे! मैं जोआना हूं, ट्विलियो और चैटजीपीटी का उपयोग करके बनाया गया एक चैटबॉट। आप आज किस बारे में बात करना चाहेंगे?"
        );
      }
  
      // Listen to the user's speech and pass the input to the /respond Function
      twiml.gather({
        speechTimeout: 'auto', // Automatically determine the end of user speech
        speechModel: 'experimental_conversations', // Use the conversation-based speech recognition model
        input: 'speech', // Specify speech as the input type
        action: '/respond', // Send the collected input to /respond
      });
    }
  
    // Create a Twilio Response object
    const response = new Twilio.Response();
  
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
  