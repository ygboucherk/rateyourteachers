class Wallet {
	constructor() {
		this.connect();
	}
	
	async connect() {
		if (window.ethereum) {
			const accounts = await window.ethereum.request({method: 'eth_requestAccounts'});
			const account = accounts[0]
			this.web3 = new Web3(window.ethereum);
		}
		else {
			throw "NO METAMASK DETECTED";
		}
	}
}

wallet = new Wallet();
