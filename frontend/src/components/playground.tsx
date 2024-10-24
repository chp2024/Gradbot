import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useChatInteract, useChatMessages, IStep } from "@chainlit/react-client";
import { useState } from "react";
import Typewriter from 'typewriter-effect';
import SuggestedPrompts from "@/components/ui/suggestedprompts";

export function Playground() {
  const [inputValue, setInputValue] = useState("");
  const { sendMessage } = useChatInteract();
  const { messages } = useChatMessages();

  const handleSendMessage = (prompt?: string) => {
    const content = prompt || inputValue.trim();
    if (content) {
      const message = {
        name: "user",
        type: "user_message" as const,
        output: content,
      };
      sendMessage(message, []);
      setInputValue("");
    }
  };

  const renderWelcomeScreen = () => {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center">
        <div className="text-7xl font-bold text-black dark:text-white">
          Welcome,
        </div>
        <p className="text-xl mt-4 text-gray-500 dark:text-gray-400">
          How can I help you today?
        </p>
        <SuggestedPrompts onPromptClick={handleSendMessage} />
      </div>
    );
  };

  const renderMessage = (message: IStep) => {
    console.log('Rendering message:', message); // Debug log
    const isGradbot = message.name === "Gradbot";

    if (message.output.length === 0) {
      return null;
    }
  
    return (
      <div key={message.id} className="flex items-start space-x-2 justify-start">
        <div className="flex items-center space-x-2 flex-row w-full">
          <div className="w-10 h-10">
            {isGradbot ? (
              <img
                src="../public/bison.png"
                alt="Gradbot Avatar"
                className="rounded-full"
              />
            ) : (
              <div className="w-10 h-10 flex items-center justify-center bg-blue-500 text-white rounded-full">
                U
              </div>
            )}
          </div>
  
          <div className="flex-1 p-4 bg-white dark:bg-gray-700 rounded-2xl shadow-md">
            {isGradbot ? (
              <Typewriter
                onInit={(typewriter) => {
                  typewriter.typeString(message.output).start();
                }}
                options={{ delay: 35, cursor: '' }}
              />
            ) : (
              <p>{message.output}</p>
            )}
          </div>
        </div>
      </div>
    );
  };
  

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 flex flex-col">
      {/*Howard Logo */}
      <div className="fixed top-4 left-4">
        <img
          src="../public/howard.png"
          alt="Gradbot Logo"
          className="h-14 w-auto"
        />
      </div>

      {/* Chat Content */}
      <div className="flex-1 overflow-auto p-6">
        <div className="space-y-4 max-w-3xl mx-auto">
          {messages.length === 0 ? (
            renderWelcomeScreen()
          ) : (
            messages.map((message) => renderMessage(message))
          )}
        </div>
      </div>

      {/*Input Box*/}
      <div className="border-t p-4 bg-white dark:bg-gray-800 rounded-t-2xl rounded-b-2xl shadow-lg fixed left-80 right-80 bottom-10 mx-6">
        <div className="flex items-center space-x-2">
          <Input
            autoFocus
            className="flex-1"
            id="message-input"
            placeholder="Type a message"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyUp={(e) => {
              if (e.key === "Enter") {
                handleSendMessage();
              }
            }}
          />
          <Button onClick={() => handleSendMessage()} type="submit">
            Send
          </Button>
        </div>
      </div>
    </div>
  );
}