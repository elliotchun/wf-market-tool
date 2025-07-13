namespace WFMarketReporter;

public partial class MainPage : ContentPage
{
	const int TRANSLATE_AMOUNT = 100;
	public MainPage()
	{
		InitializeComponent();
	}

	private async void RivenModPointerEnter(object sender, PointerEventArgs e)
	{
		await RivenModReveal();
	}

	private async void RivenModPointerLeave(object sender, PointerEventArgs e)
	{
		await RivenModHide();
	}

	private async Task RivenModReveal()
	{
		// Animate the bottom frame down by the height of the side frame
		await RivenModFrameBottom.TranslateTo(0, TRANSLATE_AMOUNT, 250, Easing.CubicInOut);

	}

	private async Task RivenModHide()
	{
		await RivenModFrameBottom.TranslateTo(0, 0, 250, Easing.CubicInOut);
	}
}
