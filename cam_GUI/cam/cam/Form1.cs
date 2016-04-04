using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.Scripting.Hosting;
using System.Diagnostics;
using System.Management;

namespace cam
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string cap_no = textBox4.Text;

            Process p = new Process();
            p.StartInfo.FileName = "python";
            p.StartInfo.Arguments = "cammm.py "+cap_no;

            /*
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardInput = true;   //重定向標準輸入
            p.StartInfo.RedirectStandardOutput = true;  //重定向標準輸出
            p.StartInfo.RedirectStandardError = true;   //重定向錯誤輸出
            */
            p.Start();
            //label10.Text = p.StandardOutput.ReadToEnd();
        }
    }
}
