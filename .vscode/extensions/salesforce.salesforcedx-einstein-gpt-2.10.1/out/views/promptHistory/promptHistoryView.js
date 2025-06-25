"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PromptHistoryView = exports.FEEDBACK_SEND_MESSAGEKEY = exports.FEEDBACK_GOOD_MESSAGEKEY = exports.FEEDBACK_COMMENT_MESSAGEKEY = exports.FEEDBACK_CANCEL_MESSAGEKEY = exports.FEEDBACK_BAD_MESSAGEKEY = exports.COMMANDPROMPTPREVIEW_MESSAGEKEY = exports.COMMANDPROMPTPREVIEW_ATTR = exports.COMMENT_CLS = exports.COLLAPSED_CLS = exports.COMPLETION_CLS = exports.COMMANDPROMPT_CLS = exports.PROMPT_HISTORY_LIMIT = void 0;
var HistoryViewEventTypes;
(function (HistoryViewEventTypes) {
    HistoryViewEventTypes["newPrompt"] = "NEWPROMPT";
    HistoryViewEventTypes["reaction"] = "REACTION";
    HistoryViewEventTypes["comment"] = "COMMENT";
    HistoryViewEventTypes["finalCompletion"] = "FINALCOMPLETION";
    HistoryViewEventTypes["accept"] = "ACCEPT";
    HistoryViewEventTypes["addRange"] = "ADDRANGE";
    HistoryViewEventTypes["defaultOrgChange"] = "DEFAULTORGCHANGE";
    HistoryViewEventTypes["initLocalizedMessages"] = "INITLOCALIZEDMESSAGES";
})(HistoryViewEventTypes || (HistoryViewEventTypes = {}));
exports.PROMPT_HISTORY_LIMIT = 20;
exports.COMMANDPROMPT_CLS = 'command-prompt';
exports.COMPLETION_CLS = 'completion';
exports.COLLAPSED_CLS = 'collapsed';
exports.COMMENT_CLS = 'prompt-td';
exports.COMMANDPROMPTPREVIEW_ATTR = 'data-command-prompt-prefix';
exports.COMMANDPROMPTPREVIEW_MESSAGEKEY = 'commandPromptPrefix';
exports.FEEDBACK_BAD_MESSAGEKEY = 'feedbackBad';
exports.FEEDBACK_CANCEL_MESSAGEKEY = 'cancel';
exports.FEEDBACK_COMMENT_MESSAGEKEY = 'feedbackComment';
exports.FEEDBACK_GOOD_MESSAGEKEY = 'feedbackGood';
exports.FEEDBACK_SEND_MESSAGEKEY = 'feedbackSend';
exports.PromptHistoryView = {
    history: [],
    localizedMessages: {},
    init: () => {
        window.addEventListener('message', exports.PromptHistoryView.handleMessage);
    },
    handleMessage: (event) => {
        const message = event.data; // The json data that the extension sent
        switch (message.type) {
            case HistoryViewEventTypes.initLocalizedMessages: {
                for (const [key, value] of Object.entries(message.data)) {
                    if (typeof value === 'string') {
                        exports.PromptHistoryView.localizedMessages[key] = value;
                    }
                }
                break;
            }
            case HistoryViewEventTypes.defaultOrgChange:
            case HistoryViewEventTypes.newPrompt: {
                const table = document.querySelector('.table__body');
                if (!table) {
                    return;
                }
                table.innerHTML = '';
                exports.PromptHistoryView.history = message.data;
                if (exports.PromptHistoryView.history.length) {
                    exports.PromptHistoryView.history.sort(function (x, y) {
                        const date1 = new Date(x.timestamp);
                        const date2 = new Date(y.timestamp);
                        return date1.getTime() - date2.getTime();
                    });
                    exports.PromptHistoryView.history.forEach((entry) => {
                        exports.PromptHistoryView.processNewPrompt(entry);
                    });
                }
                break;
            }
        }
    },
    createHistoryRow: (data) => {
        const newPromptRow = document.createElement('tr');
        const textBoxContainer = document.createElement('div');
        newPromptRow.classList.add('table__data-row', exports.COLLAPSED_CLS);
        newPromptRow.setAttribute('data-history-id', data.historyId);
        newPromptRow.addEventListener('click', function () {
            exports.PromptHistoryView.handleRowOpenAndCollapse(this);
        });
        const dataAsArray = [];
        const date = new Date(data.timestamp);
        const dateString = date.toDateString();
        const timeString = date.toLocaleString([], { hour: 'numeric', minute: 'numeric', hour12: true });
        dataAsArray[0] = { value: dateString, title: `${dateString} ${timeString}` };
        dataAsArray[1] = { value: data.prompt, title: data.prompt };
        if (!data.prompt && data.commandPrompt) {
            dataAsArray[1] = {
                value: data.commandPrompt,
                title: data.commandPrompt,
                cls: exports.COMMANDPROMPT_CLS,
                additionalAttributes: [
                    {
                        name: exports.COMMANDPROMPTPREVIEW_ATTR,
                        value: exports.PromptHistoryView.localizedMessages[exports.COMMANDPROMPTPREVIEW_MESSAGEKEY]
                    }
                ]
            };
        }
        dataAsArray[2] = { value: data.completion, title: data.completion, cls: exports.COMPLETION_CLS };
        dataAsArray.forEach((item) => {
            const el = document.createElement('td');
            el.setAttribute('title', item.title);
            el.textContent = item.value;
            if (item.cls) {
                el.classList.add(item.cls);
            }
            if (item.additionalAttributes) {
                item.additionalAttributes.forEach((attr) => el.setAttribute(attr.name, attr.value));
            }
            newPromptRow.appendChild(el);
        });
        newPromptRow.appendChild(textBoxContainer);
        const textarea = newPromptRow.querySelector('textarea');
        if (textarea && data.feedback?.comment) {
            textarea.value = data.feedback.comment;
        }
        newPromptRow.appendChild(textBoxContainer);
        return newPromptRow;
    },
    processNewPrompt: (data) => {
        console.log('message received');
        const tableBody = document.querySelector('.table__body');
        const newPrompt = exports.PromptHistoryView.createHistoryRow(data);
        tableBody?.prepend(newPrompt);
        if (exports.PromptHistoryView.history.length > exports.PROMPT_HISTORY_LIMIT) {
            exports.PromptHistoryView.deleteLastHistoryRow();
        }
    },
    deleteLastHistoryRow: () => {
        const tableBody = document.querySelector('.table__body');
        if (tableBody && tableBody.lastChild) {
            tableBody.removeChild(tableBody.lastChild);
            exports.PromptHistoryView.history.pop();
        }
    },
    handleRowOpenAndCollapse: (element) => {
        const selectedText = window.getSelection()?.toString();
        if (!selectedText) {
            element.classList.toggle('collapsed');
        }
    }
};
(function () {
    exports.PromptHistoryView.init();
})();
//# sourceMappingURL=promptHistoryView.js.map