namespace WFMarketReporter;

public partial class MainPage : ContentPage
{
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
		await RivenModFrameBottom.TranslateTo(0, RivenModFrameSideLeft.Height, 250, Easing.CubicInOut);
		RivenModFrameSideLeft.IsVisible = RivenModFrameSideRight.IsVisible = true;

	}

	private async Task RivenModHide()
	{
		await RivenModFrameBottom.TranslateTo(0, 0, 250, Easing.CubicInOut);
		RivenModFrameSideLeft.IsVisible = RivenModFrameSideRight.IsVisible = false;
	}
}
