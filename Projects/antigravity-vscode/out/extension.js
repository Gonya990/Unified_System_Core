"use strict";
/**
 * Antigravity AI - VS Code Extension
 * Multi-provider AI chat sidebar
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const chatViewProvider_1 = require("./chatViewProvider");
const providerManager_1 = require("./providers/providerManager");
let chatViewProvider;
let providerManager;
function activate(context) {
    console.log('Antigravity AI is now active!');
    // Initialize provider manager
    providerManager = new providerManager_1.ProviderManager();
    // Register chat view provider
    chatViewProvider = new chatViewProvider_1.ChatViewProvider(context.extensionUri, providerManager);
    context.subscriptions.push(vscode.window.registerWebviewViewProvider('antigravity.chatView', chatViewProvider));
    // Register commands
    context.subscriptions.push(vscode.commands.registerCommand('antigravity.openChat', () => {
        vscode.commands.executeCommand('workbench.view.extension.antigravity-sidebar');
    }));
    context.subscriptions.push(vscode.commands.registerCommand('antigravity.newConversation', () => {
        chatViewProvider.clearConversation();
    }));
    context.subscriptions.push(vscode.commands.registerCommand('antigravity.switchProvider', async () => {
        const providers = providerManager.getAvailableProviders();
        const selected = await vscode.window.showQuickPick(providers.map(p => ({
            label: p.name,
            description: p.model,
            detail: p.available ? '✓ Connected' : '✗ No API key'
        })), { placeHolder: 'Select AI Provider' });
        if (selected) {
            const config = vscode.workspace.getConfiguration('antigravity');
            await config.update('defaultProvider', selected.label.toLowerCase(), true);
            vscode.window.showInformationMessage(`Switched to ${selected.label}`);
        }
    }));
    context.subscriptions.push(vscode.commands.registerCommand('antigravity.explainSelection', async () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const selection = editor.document.getText(editor.selection);
            if (selection) {
                chatViewProvider.sendMessage(`Explain this code:\n\`\`\`\n${selection}\n\`\`\``);
            }
        }
    }));
    context.subscriptions.push(vscode.commands.registerCommand('antigravity.refactorSelection', async () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const selection = editor.document.getText(editor.selection);
            if (selection) {
                chatViewProvider.sendMessage(`Refactor this code to be cleaner and more efficient:\n\`\`\`\n${selection}\n\`\`\``);
            }
        }
    }));
    context.subscriptions.push(vscode.commands.registerCommand('antigravity.insertCode', async (code) => {
        const editor = vscode.window.activeTextEditor;
        if (editor && code) {
            editor.edit(editBuilder => {
                editBuilder.insert(editor.selection.active, code);
            });
        }
    }));
    // Watch for configuration changes
    context.subscriptions.push(vscode.workspace.onDidChangeConfiguration(e => {
        if (e.affectsConfiguration('antigravity')) {
            providerManager.reloadConfiguration();
        }
    }));
}
function deactivate() {
    console.log('Antigravity AI deactivated');
}
//# sourceMappingURL=extension.js.map