// tools/sessionNotes.js
// Tool for managing in-call session notes

import { Type, Behavior } from "../core/geminiTypes.js";

export const sessionNotesTool = {
  declaration: {
    name: "session_notes",
    description:
      "Manage session notes for conversation context and notes. Use append to add new information, read to retrieve stored notes.",
    parameters: {
      type: Type.OBJECT,
      properties: {
        operation: {
          type: Type.STRING,
          description: "Operation to perform on notes",
          enum: ["append", "read"],
        },
        note: {
          type: Type.STRING,
          description: "Note content to append (required for append operation)",
        },
      },
      required: ["operation"],
    },
    behavior: Behavior.NON_BLOCKING,
  },
};
