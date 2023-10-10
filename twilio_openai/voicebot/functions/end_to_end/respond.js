// Import required modules
const { OpenAI } = require("openai");
const fetch = require('node-fetch');
// Define the main function for handling requests
exports.handler = async function(context, event, callback) {
    // Set up the OpenAI API with the API key
    // const configuration = new Configuration({ apiKey: context.OPENAI_API_KEY });
    const fs = require('fs');
    const config = JSON.parse(fs.readFileSync('config.json', 'utf-8'));

    // Set up the Twilio VoiceResponse object to generate the TwiML
    const twiml = new Twilio.twiml.VoiceResponse();

    const Voice_assistant = config.languages.english.voice;

    // Initiate the Twilio Response object to handle updating the cookie with the chat history
    const response = new Twilio.Response();

    // Parse the cookie value if it exists
    const cookieValue = event.request.cookies.convo;
     const conversation = [];

    // Get the user's voice input from the event
    const voiceInput = event.SpeechResult;
    // let voiceInput = "Quantum computing"
    console.log("Sending voice input to server:", voiceInput);

    // Create a conversation variable to store the dialog and the user's input to the conversation history
      // Make an HTTP POST request to your /api/chat endpoint
      try {
        const chatResponse = await fetch('https://ngrok url of the server/api/call', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${context.OPENAI_API_KEY}`,
            },
            body: JSON.stringify({
                messages: [
                    {
                        role: 'user',
                        content: voiceInput,
                    },
                ],
            }),
        });
//    console.log(messages)
        if (!chatResponse.ok) {
            console.error('Error from /api/call:', chatResponse.status, chatResponse.statusText);
            return callback('Error from /api/call');
        }

        const chatData = await chatResponse.json();
        console.log(chatData);

        // Extract the AI's response from chatData and clean it if necessary
        const aiResponse = chatData.response.content;
        console.log(aiResponse);

        conversation.push({ role: 'assistant', content: aiResponse });

        // Use aiResponse to generate TwiML response as before
        twiml.say({
            voice: Voice_assistant,
        }, aiResponse);
    

    // Redirect to the Function where the <Gather> is capturing the caller's speech
    twiml.redirect({
            method: "POST",
        },
        `/end_to_end/transcribe`
    );
    
    // Since we're using the response object to handle cookies we can't just pass the TwiML straight back to the callback, we need to set the appropriate header and return the TwiML in the body of the response
    response.appendHeader("Content-Type", "application/xml");
    response.setBody(twiml.toString());

    // Update the conversation history cookie with the response from the OpenAI API
    const newCookieValue = encodeURIComponent(
        JSON.stringify({
            conversation,
        })
    );
    response.setCookie("convo", newCookieValue, ["Path=/"]);

    // Return the response to the handler
    return callback(null, response);
} catch (error) {
    console.error('Error during /api/call request:', error);
    return callback('Error during /api/call request');
}
};
