// tools/dynamicEvaluationTool.js
// Factory for creating evaluation tools from campaign-provided declarations

/**
 * Creates a dynamic evaluation tool from a validated declaration
 * The declaration comes from campaign config and is validated by geminiTypes.js
 * @param {Object} declaration - Validated tool declaration (name must be 'call_outcomes')
 * @returns {Object} Tool object with declaration property
 */
export function createDynamicEvaluationTool(declaration) {
  return {
    declaration,
  };
}
