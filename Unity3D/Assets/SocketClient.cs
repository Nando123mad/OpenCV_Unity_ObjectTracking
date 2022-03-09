using UnityEngine;
using System;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class SocketClient : MonoBehaviour {

	// Use this for initialization

	public GameObject hero;
	private float xPos = 10.0f;
	private float yPos = 10.0f;

	Thread receiveThread;
	UdpClient client;
	public int port;

	//info

	public string lastReceivedUDPPacket = "";
	public string allReceivedUDPPackets = "";

	void Start () {
		init();
	}

	void OnGUI(){
		Rect  rectObj=new Rect (40,10,200,400);
		
		GUIStyle  style  = new GUIStyle ();
		
		style .alignment  = TextAnchor.UpperLeft;
		
		GUI .Box (rectObj,"# UDPReceive\n127.0.0.1 "+port +" #\n"
		          
		          //+ "shell> nc -u 127.0.0.1 : "+port +" \n"
		          
		          + "\nLast Packet: \n"+ lastReceivedUDPPacket
		          
		          //+ "\n\nAll Messages: \n"+allReceivedUDPPackets
		          
		          ,style );
	}

	private void init(){
		print ("UPDSend.init()");

		port = 5065;

		print ("Sending to 127.0.0.1 : " + port);

		receiveThread = new Thread (new ThreadStart(ReceiveData));
		receiveThread.IsBackground = true;
		receiveThread.Start ();

	}

	private void ReceiveData(){
		client = new UdpClient (port);
		while (true) {
			try{
				IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("127.0.0.1"), port);
				byte[] data = client.Receive(ref anyIP);

				//added X and Y to specifically take out incoming values otherwise it would be the full string streamed in. 
				string textX = Encoding.UTF8.GetString(data);
				int index = (textX.IndexOf(":")) + 1;
				int index2 = (textX.IndexOf("\n")) - 1;
				if (index >= 0)
					textX = textX.Substring(index, index2);
				print (">> " + textX);

				string textY = Encoding.UTF8.GetString(data);
				int index3 = (textY.IndexOf("\n")) + 3;
				int index4 = (textY.IndexOf("\n")) - 2;
				if (index3 >= 0)
					textY = textY.Substring(index3, index4);
				print (">> " + textY);
				lastReceivedUDPPacket=textX;
				allReceivedUDPPackets=allReceivedUDPPackets+textX;

				xPos = float.Parse(textX);
				xPos *= 10f;
				xPos = -xPos;

				yPos = float.Parse(textY);
				yPos *= 10f;
				yPos = -yPos;

			}catch(Exception e){
				print (e.ToString());
			}
		}
	}

	public string getLatestUDPPacket(){
		allReceivedUDPPackets = "";
		return lastReceivedUDPPacket;
	}
	
	// Update is called once per frame
	void Update () {
		hero.transform.position = new Vector3(xPos+5.0f,yPos+5.0f);
	}

	void OnApplicationQuit(){
		if (receiveThread != null) {
			receiveThread.Abort();
			Debug.Log(receiveThread.IsAlive); //must be false
		}
	}
}
