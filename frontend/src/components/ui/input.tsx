import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Input = React.forwardRef<HTMLTextAreaElement, InputProps>(
  ({ className, ...props }, ref) => {
    const textareaRef = React.useRef<HTMLTextAreaElement>(null);

    const handleInput = () => {
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
        textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
      }
    };

    React.useEffect(() => {
      handleInput();
    }, []);

    return (
      <textarea
        ref={(node) => {
          textareaRef.current = node;
          if (ref) {
            (ref as React.RefObject<HTMLTextAreaElement>).current = node;
          }
        }}
        className={cn(
          "flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        onInput={handleInput}
        rows={1}
        {...props}
      />
    );
  }
);

Input.displayName = "Input";

export { Input };