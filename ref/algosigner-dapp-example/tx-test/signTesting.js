function useTxDefaults() {
  return document.getElementById("usetxdefaults").checked;
}
function sendSignedTx() {
  return document.getElementById("sendsignedtx").checked;
}

let payTx = document.getElementById("payTx");
payTx.addEventListener("click", createPayTx, false);

let applTx = document.getElementById("applTx");
applTx.addEventListener("click", makeApplication, false);

let acceptTx = document.getElementById("acceptTx");
acceptTx.addEventListener("click", acceptAsset, false);

let axferTx = document.getElementById("axferTx");
axferTx.addEventListener("click", transferAsset, false);

let closeTx = document.getElementById("closeTx");
if (closeTx) 
    closeTx.addEventListener("click", closeAsset, false);

let clawbackTx = document.getElementById('clawbackTx');
clawbackTx.addEventListener("click", clawbackAsset, false);

let acfgModifyTx = document.getElementById("acfgModifyTx");
acfgModifyTx.addEventListener("click", modifyAsset, false);

let acfgCreateTx = document.getElementById("acfgCreateTx");
acfgCreateTx.addEventListener("click", createAsset, false);

let acfgDestroyTx = document.getElementById("acfgDestroyTx");
acfgDestroyTx.addEventListener("click", destroyAsset, false);

let afrzTx = document.getElementById("afrzTx");
afrzTx.addEventListener("click", freezeAsset, false);

let groupTx = document.getElementById("groupTx");
groupTx.addEventListener("click", createGroupPayTx, false);

let groupGroupsTxs = document.getElementById('groupGroupsTxs');
if(groupGroupsTxs)
    groupGroupsTxs.addEventListener("click", createGroupGroupsTxs, false);

let multisigTx = document.getElementById("multisigTx");
multisigTx.addEventListener("click", createMultisigTx, false);

let rekeyTx = document.getElementById('rekeyTx');
if(rekeyTx)
    rekeyTx.addEventListener("click", createRekeyTx, false);

let rekeyedPayTx = document.getElementById('rekeyedPayTx');
if(rekeyedPayTx)
    rekeyedPayTx.addEventListener("click", createRekeyedPayTx, false);