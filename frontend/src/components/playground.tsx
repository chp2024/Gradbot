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
import { del } from "aws-amplify/api";

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
    return (
      <div key={message.id} className="flex items-start space-x-2">
        <div className="flex items-center space-x-2 w-full">
          <div className="w-20 text-sm text-green-500">{message.name}</div>
          <div className="flex-1 p-2">
              {message.name === "Gradbot" ? (
                <Typewriter
                onInit={(typewriter) => {
                  typewriter
                    .typeString(message.output)
                    .start()
                    .callFunction(() => {
                      console.log('String typed out!');
                    })
                }}
                options={{
                  delay: 50,
                  cursor: '',
                }}
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
        <div className="space-y-4">
          {messages.map((message) => renderMessage(message))}
        </div>
      </div>
      <div className="border-t p-4 bg-white dark:bg-gray-800 rounded-t-2xl rounded-b-2xl shadow-lg fixed left-0 right-0 bottom-10 mx-6">
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
