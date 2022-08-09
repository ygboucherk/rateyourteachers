function connectWallet() {
	if !(window.ethereum) {
		console.error("NO METAMASK DETECTED");
		return false;
	}
	return Web3(window.ethereum);
}
