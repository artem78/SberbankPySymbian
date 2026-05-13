unit Unit1;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, ExtCtrls,
  UniqueInstance, LazUTF8, math, streamex, RegExpr;

type

  { TForm1 }

  TForm1 = class(TForm)
    Button1: TButton;
    Button2: TButton;
    Button3: TButton;
    Button4: TButton;
    Button5: TButton;
    Button6: TButton;
    Button7: TButton;
    Button8: TButton;
    Label1: TLabel;
    Label2: TLabel;
    Memo1: TMemo;
    Memo2: TMemo;
    Timer1: TTimer;
    UniqueInstance1: TUniqueInstance;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure Button4Click(Sender: TObject);
    procedure Button5Click(Sender: TObject);
    procedure Button6Click(Sender: TObject);
    procedure Button7Click(Sender: TObject);
    procedure Button8Click(Sender: TObject);
    procedure Memo1Change(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
  private

  public

  end;

var
  Form1: TForm1;

implementation

uses StrUtils;

const
  SDK_C_DRIVE = 'c:\\Symbian\\9.2\\S60_3rd_FP1\\Epoc32\\winscw\\c';
  {$IFOPT D+}
  INCOMING_SMS_FILE = 'sber_cmd.log';
  {$else}
  INCOMING_SMS_FILE = SDK_C_DRIVE+ '\\sber_cmd.log';
  {$endif}

procedure clear_all_income;
begin
  if not FileExists(INCOMING_SMS_FILE) then exit;

  // очищаем файл
  //DeleteFile(INCOMING_SMS_FILE);
  with TStringList.Create() do
  begin
    Clear;
    SaveToFile(INCOMING_SMS_FILE);
    Free;
  end;
end;

procedure send_reply(msg: string);
const
  {$IFOPT D+}
  SMS_OUT_FILENAME = 'message.sms';
  {$else}
  SMS_OUT_FILENAME = SDK_C_DRIVE + '\\smsin\\message.sms';
  {$endif}
var
  strm: TBytesStream;
  //strm:  TStringStream;
  ch: UCS2Char;
  i: integer;
  ws: WideString;
  ss:TStringStream;
  b:Byte;
  //&in, &out: TBytes;
  len:uint16;
begin
  strm := TBytesStream.Create;
  ss:=TStringStream.Create;

  try
    strm.WriteByte($03);
    strm.WriteByte($a3);
    strm.WriteByte($02);
    strm.WriteByte($00);
    strm.WriteByte($01);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($04);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($f9);
    strm.WriteByte($66);
    strm.WriteByte($a6);
    strm.WriteByte($2e);

    strm.WriteByte($01);
    strm.WriteByte($2c);
    strm.WriteByte($e3);
    strm.WriteByte($00);
    strm.WriteByte($02);
    strm.WriteByte($81);
    strm.WriteByte($0c);
    strm.WriteByte($31);
    strm.WriteByte($32);
    strm.WriteByte($33);
    strm.WriteByte($15);
    strm.WriteByte($00);
    strm.WriteByte($81);
    strm.WriteByte($0c);
    strm.WriteByte($39);
    strm.WriteByte($30);

    strm.WriteByte($30);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($a0);
    strm.WriteByte($b0);
    strm.WriteByte($09);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($02);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);

    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    // байты 57-58
    //strm.WriteByte(length(msg));
    len:=length(msg);
    strm.WriteByte(lo(len)); // младший
    strm.WriteByte(hi(len)); // старший
    //strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);

    //for i := 0 to length(msg)-1 do
    {for i := 1 to length(msg) do
    begin
      ch:=msg[i] ;
      strm.WriteBuffer(ch,2);
    end;}
    //tmp:=UTF8ToUTF16(msg);
    //strm.WriteBuffer(tmp, Length(tmp));
    //strm.WriteAnsiString(msg);
    //strm.WriteBuffer(tmp, length(tmp));
    //strm.write;

    //ss.WriteUnicodeString(tmp);
    //strm.Write(ss.Bytes);
    //for b in ss.Bytes do
    //  strm.WriteByte(b);
    ws := UTF8Decode(msg);
    //strm.WriteUnicodeString(ws);

   {   &in := BytesOf(msg);
  &out := TEncoding.Convert(TEncoding.UTF8, TEncoding.{BigEndian}Unicode, &in);
      for b in &out do
  begin
    strm.writebyte(b);
  end;        }

    strm.writeBuffer(WS[1], Length(ws) * 2);

    strm.WriteByte($02);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);
    strm.WriteByte($00);

    strm.SaveToFile(SMS_OUT_FILENAME);

  finally
    strm.Free;
    ss.free;
  end;

end;

procedure send_balans;
var
  sl: TStringList;
begin
  sl:=TStringList.Create;
  sl.Append('Баланс по картам:');
  sl.append('ECMC0000: '+inttostr(RandomRange(100, 50000))+'р');
  sl.append('MAESTRO1111: '+inttostr(RandomRange(100, 50000))+','+inttostr(RandomRange(10, 99))+'р');
  sl.append('ECMC2222: '+inttostr(RandomRange(100, 50000))+'р');
  send_reply(sl.Text);
  sl.free;
end;

procedure send_vipiska(cardnumber4: string);
var
  sl: TStringList;
begin
  sl:=TStringList.Create;
  sl.append('Мини-выписка по карте ECMC' + cardnumber4 + ':' );
  sl.append('18.03.2026 - 50р' );
  sl.append('18.03.2026 - 73р' );
  sl.append('18.03.2026 - 1р'  );
  sl.append('18.03.2026 - 73р' );
  sl.append('17.03.2026 - 84р');
  sl.append('14.03.2026 - 20р');
  sl.append('14.03.2026 - 84р');
  sl.append('13.03.2026 - 84р');
  sl.append('13.03.2026 - 84р');
  sl.append('12.03.2026 - 300р');
  sl.append('Баланс: 30220,75р');

  send_reply(sl.Text);
  sl.free;
end;

{procedure send_perevod_success;
begin
  send_reply('ECMC0000: перевод 2500р на карту MIR0000, получатель Иван Иванович И. доставлен. ');
end;}

procedure send_phone_popoln_success(sum: integer; phonenumber: string = '9850000000');
begin
  {if phonenumber = '':

  else

  }
  send_reply('Выполнена оплата услуги МТС, номер телефона: '+phonenumber+'. КартаMASTERCARD0000, сумма платежа '+inttostr(sum)+'р. Комиссия 0р.');
end;

procedure send_perevod_success(sum:integer = 9999);
begin
  send_reply('ECMC0000: перевод '+inttostr(sum)+'р на карту MIR0000, получатель Иван Иванович И. доставлен. ');
end;

procedure send_confirmation(sum:integer; cardnumber: string = '0000000000000000');
var s:string; rnd: integer; cardnumber_short:string;
begin
  cardnumber_short:=copy(cardnumber, length(cardnumber)-4+1, 4);;
  rnd:=RandomRange(10000,99999);
  if RandomRange(0,2)=0 then // V1
    s :=   'Подтвердите перевод '+inttostr(sum)+'р с карты ECMC0000 на MIR'+cardnumber_short+', получатель Иван Иванович И. Комиссия 0р. Отправьте код '+inttostr(rnd)+' на 900. Никому его не сообщайте. Если вы не совершали операцию, позвоните на 900.'
  else // V2
    s:='Подтвердите перевод с карты ECMC0000 на карту MIR'+cardnumber_short+' на сумму '+inttostr(sum)+'р. Код: '+inttostr(Rnd)+'. Никому его не сообщайте и не подтверждайте операции, которые вы не совершали.';;
  send_reply(s);
end;

{$R *.lfm}

{ TForm1 }

procedure TForm1.Button1Click(Sender: TObject);
var
  msg: string;
begin
  msg := 'Мини-выписка по карте ECMC0000:' + LineEnding +
'18.03.2026 - 50р' + LineEnding +
'18.03.2026 - 73р' + LineEnding+
'18.03.2026 - 1р'  + LineEnding+
'18.03.2026 - 73р' + LineEnding+
'17.03.2026 - 84р'  + LineEnding+
'14.03.2026 - 20р'  + LineEnding+
'14.03.2026 - 84р'  + LineEnding+
'13.03.2026 - 84р'  + LineEnding+
'13.03.2026 - 84р'  + LineEnding+
'12.03.2026 - 300р'  + LineEnding+
'Баланс: 30220,75р'  ;
  memo1.Text:=msg;
end;

procedure TForm1.Button2Click(Sender: TObject);
var msg:string;
begin
  Memo1.Text:='Test';

end;

procedure TForm1.Button3Click(Sender: TObject);
begin
  send_reply(memo1.Text);
end;

procedure TForm1.Button4Click(Sender: TObject);
begin
  Memo1.Text:='Подтвердите перевод 2500р с карты ECMC0000 на MIR0000, получатель Иван Иванович И. Комиссия 0р. Отправьте код '+inttostr(RandomRange(10000,99999))+' на 900. Никому его не сообщайте. Если вы не совершали операцию, позвоните на 900.';
end;

procedure TForm1.Button5Click(Sender: TObject);
begin
  Memo1.Clear;
  memo1.Append('Баланс по картам:');
  memo1.append('ECMC0000: 6403,75р');
  memo1.append('MAESTRO1111: 6403,75р');
  memo1.append('ECMC2222: 40000р')
end;

procedure TForm1.Button6Click(Sender: TObject);
begin
  memo1.text:='Подтвердите перевод с карты ECMC0000 на карту MIR0000 на сумму 100р. Код: '+inttostr(RandomRange(10000,99999))+'. Никому его не сообщайте и не подтверждайте операции, которые вы не совершали.';
end;

procedure TForm1.Button7Click(Sender: TObject);
begin
  memo1.text:='ECMC0000: перевод 2500р на карту MIR0000, получатель Иван Иванович И. доставлен. ';
end;

procedure TForm1.Button8Click(Sender: TObject);
begin
  memo1.text:='Выполнена оплата услуги МТС, номер телефона: 9850000000. КартаMASTERCARD0000, сумма платежа 15р. Комиссия 0р.';
end;

procedure TForm1.Memo1Change(Sender: TObject);
begin
  label1.Caption:=inttostr(length(memo1.Text)) + ' символов';
end;

procedure TForm1.Timer1Timer(Sender: TObject);
var
  //f:textfile;
  reader: {tstreamreader} TFileReader;
  re: TRegExpr;
  cmd: string;
  &type: string;
begin

  if not FileExists(INCOMING_SMS_FILE) then
    exit;

    reader := {TStreamReader}TFileReader.Create(INCOMING_SMS_FILE);
  try
    //reader.rea;
    while not reader.Eof do
    begin
      cmd := reader.ReadLine();
      cmd:=Trim(cmd);
      if cmd ='' then continue;
      //WriteLn(Format('First line: %s', [s]));
      &type := IfThen(StartsStr('*900*', cmd), 'USSD', 'СМС ');
      memo2.Append(
                     Format('%s     [%s]      %s',
                            [DateTimeToStr(Now), &type, cmd]
                           )
                  );

      {***  SMS команды ***}
      // баланс
      if cmd = 'BALANS' then
      begin
        send_balans;
        continue;
      end;

      re := TRegExpr.Create();
      re.ModifierI:=true;

      // мини выписка
      re.Expression:='history (\d{4})';
      if re.exec(cmd) then
      begin
        send_vipiska(re.Match[1]);
        freeandnil(re);
        continue;
      end;

      // код подтверждения
      re.Expression:='^(\d{5})$';
      if re.exec(cmd) then
      begin
        send_perevod_success;
        freeandnil(re);
        continue;
      end;

      // пополнение своего тел.
      re.Expression:='^(\d+)$';
      if re.exec(cmd) then
      begin
        send_phone_popoln_success(strtoint(re.Match[1]));
        freeandnil(re);
        continue;
      end;

      // пополнение тлефона по номеру
      re.Expression:='^(\d{10}) (\d+)$';
      if re.exec(cmd) then
      begin
        send_phone_popoln_success(strtoint(re.match[2]), re.Match[1]);
        freeandnil(re);
        continue;
      end;

      // перевод по номеру карты
      re.Expression:='^perevod (\d{16,18}) (\d+)$';
      if re.exec(cmd) then
      begin
        //send_perevod_success(strtoint(re.Match[2]));
        send_confirmation(strtoint(re.Match[2]), re.Match[1]);
        freeandnil(re);
        continue;
      end;

      // перевод по номеру тел.
      re.Expression:='^perevod (\d{10}) (\d+)$';
      if re.exec(cmd) then
      begin
        //send_perevod_success(strtoint(re.Match[2]));
        send_confirmation(StrToInt(re.Match[2]));
        freeandnil(re);
        continue;
      end;


      { ***  USSD команды *** }
      // баланс
      if cmd = '*900*01#' then
      begin
        send_balans;
        FreeAndNil(re);
        continue;
      end;

      //истор. оп.
      re.Expression:='^\*900\*02\*(\d{4})\#$';
      if re.Exec(cmd) then
      begin
        send_vipiska(re.Match[1]);
        freeandnil(re);
        continue;
      end;

      //   опл. тел свой
      re.Expression:='^\*900\*(\d+)\#$';
      if re.Exec(cmd) then
      begin
        send_phone_popoln_success(strtoint(re.Match[1]));
        freeandnil(re);
        continue;
      end;

      // опл. чуж. тел.
      re.Expression:='^\*900\*(9\d{9})\*(\d+)\#$';
      if re.exec(cmd) then
      begin
        send_phone_popoln_success(strtoint(re.match[2]), re.Match[1]);
        freeandnil(re);
        continue;
      end;

      // перевод по номеру тел.
      re.Expression:='^\*900\*12\*(9\d{9})\*(\d+)\#$';
      if re.exec(cmd) then
      begin
        //send_perevod_success(strtoint(re.Match[2]));
        send_confirmation(StrToInt(re.Match[2]));
        freeandnil(re);
        continue;
      end;



      // команда не опознана
      send_reply('Unknown command!') ;
      memo2.Append('???');
      freeandnil(re);
    end;
  finally
    reader.Free;
  end;

  clear_all_income();

end;

end.

