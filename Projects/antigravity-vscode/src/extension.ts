/**
 * Antigravity AI - VS Code Extension
 * Multi-provider AI chat sidebar
 */

import * as vscode from 'vscode';
import { ChatViewProvider } from './chatViewProvider';
import { ProviderManager } from './providers/providerManager';

let chatViewProvider: ChatViewProvider;
let providerManager: ProviderManager;

export function activate(context: vscode.ExtensionContext) {
    console.log('Antigravity AI is now active!');

    // Initialize provider manager
    providerManager = new ProviderManager();

    // Register chat view provider
    chatViewProvider = new ChatViewProvider(context.extensionUri, providerManager);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            'antigravity.chatView',
            chatViewProvider
        )
    );

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('antigravity.openChat', () => {
            vscode.commands.executeCommand('workbench.view.extension.antigravity-sidebar');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('antigravity.newConversation', () => {
            chatViewProvider.clearConversation();
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('antigravity.switchProvider', async () => {
            const providers = providerManager.getAvailableProviders();
            const selected = await vscode.window.showQuickPick(
                providers.map(p => ({
                    label: p.name,
                    description: p.model,
                    detail: p.available ? '✓ Connected' : '✗ No API key'
                })),
                { placeHolder: 'Select AI Provider' }
            );
            if (selected) {
                const config = vscode.workspace.getConfiguration('antigravity');
                await config.update('defaultProvider', selected.label.toLowerCase(), true);
                vscode.window.showInformationMessage(`Switched to ${selected.label}`);
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('antigravity.explainSelection', async () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                const selection = editor.document.getText(editor.selection);
                if (selection) {
                    chatViewProvider.sendMessage(`Explain this code:\n\`\`\`\n${selection}\n\`\`\``);
                }
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('antigravity.refactorSelection', async () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                const selection = editor.document.getText(editor.selection);
                if (selection) {
                    chatViewProvider.sendMessage(`Refactor this code to be cleaner and more efficient:\n\`\`\`\n${selection}\n\`\`\``);
                }
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('antigravity.insertCode', async (code: string) => {
            const editor = vscode.window.activeTextEditor;
            if (editor && code) {
                editor.edit(editBuilder => {
                    editBuilder.insert(editor.selection.active, code);
                });
            }
        })
    );

    // Watch for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('antigravity')) {
                providerManager.reloadConfiguration();
            }
        })
    );
}

export function deactivate() {
    console.log('Antigravity AI deactivated');
}
