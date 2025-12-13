// tools/endCall.js
// Tool for ending the current call

import { Type, Behavior } from "../core/geminiTypes.js";

export const endCallTool = {
  declaration: {
    name: "end_call",
    description: "End the current call when conversation is complete",
    parameters: {
      type: Type.OBJECT,
      properties: {
        reason: {
          type: Type.STRING,
          description: "Reason for ending the call",
        },
      },
      required: ["reason"],
    },
    behavior: Behavior.BLOCKING,
  },
};
