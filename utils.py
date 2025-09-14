import os, pickle

def read_dataset(filepath, silent=True):
    if os.path.exists(filepath):
        # If the pickle exists, extract the array of function_pairs
        dataset = pickle.load(open(filepath, "rb"))
        if not silent:
            print("Loaded " + str(len(dataset)) + " data items from " + filepath)
        return dataset
    else:
        print(filepath + " does not exist")
        quit(1)

def categorize(term):

    categories = {
    "JAXB": ["javax.xml.bind"],
    "JAX-WS": ["javax.xml.ws", "javax.jws"],
    "Activation": ["javax.activation"],
    "CORBA": ["org.omg"],
    "Transactions": ["javax.transaction"],
    "Security Policy": ["javax.security.auth.Policy"],
    "SecurityManager checks": [
        "SecurityManager.checkSystemClipboardAccess", ".checkSystemClipboardAccess",
        "SecurityManager.checkMemberAccess", ".checkMemberAccess",
        "SecurityManager.checkTopLevelWindow", ".checkTopLevelWindow",
        "SecurityManager.checkAwtEventQueueAccess", ".checkAwtEventQueueAccess"
    ],
    "Thread APIs": [
        "Thread.stop(", ".stop(",
        "Thread.destroy(", ".destroy(",
        "System.runFinalizersOnExit(", "Runtime.runFinalizersOnExit("
    ]
}

    for cat, patterns in categories.items():
        if any(p in term for p in patterns):
            return cat
    return "Other"