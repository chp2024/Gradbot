import React from 'react';

interface SuggestedPromptsProps {
  onPromptClick: (prompt: string) => void;
}

const SuggestedPrompts: React.FC<SuggestedPromptsProps> = ({ onPromptClick }) => {
    const prompts = [
        "What classes am I taking this semester?",
        "What is my classification?",
        "How many credits do I have?",
        "What classes should I take next semester?"
        ];

    return (
        <div className="grid grid-cols-2 gap-4 mt-4">
            {prompts.map((prompt, index) => (
            <div
                key={index}
                className="cursor-pointer bg-gray-200 dark:bg-gray-700 p-4 rounded-lg shadow-md hover:bg-gray-300 h-16 flex items-center justify-center" // Remove width for grid layout
                onClick={() => onPromptClick(prompt)}
            >
                {prompt}
            </div>
            ))}
        </div>
    );
};

export default SuggestedPrompts;