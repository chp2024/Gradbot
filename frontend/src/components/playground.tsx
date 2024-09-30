import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { v4 as uuidv4 } from "uuid";

import {
  useChatInteract,
  useChatMessages,
  IStep,
} from "@chainlit/react-client";
import Typewriter from 'typewriter-effect';
import { useState } from "react";

export function Playground() {
  const [inputValue, setInputValue] = useState("");
  const { sendMessage } = useChatInteract();
  const { messages } = useChatMessages();

  const handleSendMessage = () => {
    const content = inputValue.trim();
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

  const renderMessage = (message: IStep) => {
    const isGradbot = message.name === "Gradbot";
    
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
          
          <div className="flex-1 p-2 bg-white dark:bg-gray-700 rounded-full shadow-md">
            {isGradbot ? (
              <Typewriter
                onInit={(typewriter) => {
                  typewriter.typeString(message.output).start();
                }}
                options={{ delay: 50, cursor: '' }}
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
      <div className="flex-1 overflow-auto p-6">
        <div className="space-y-4 max-w-3xl mx-auto">
          {messages.map((message) => renderMessage(message))}
        </div>
      </div>
      <div className="border-t p-4 bg-white dark:bg-gray-800 rounded-t-2xl rounded-b-2xl shadow-lg fixed left-60 right-60 bottom-10 mx-6">
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
          <Button onClick={handleSendMessage} type="submit">
            Send
          </Button>
        </div>
      </div>
    </div>
  );
}