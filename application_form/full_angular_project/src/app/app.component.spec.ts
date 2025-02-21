
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { By } from '@angular/platform-browser';

describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AppComponent],
      imports: [ReactiveFormsModule], // Import ReactiveFormsModule for reactive forms
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges(); // Trigger initial data binding
  });

  it('should create the app component', () => {
    expect(component).toBeTruthy();
  });

  it('should have a title', () => {
    const title = component.title;
    expect(title).toBeDefined();
    expect(title).toEqual('Your App Title'); // Replace with your actual title
  });

  it('should initialize the form', () => {
    expect(component.myForm).toBeDefined();
    expect(component.myForm.controls['exampleControl']).toBeDefined(); // Replace with your actual control name
  });

  it('should submit the form', () => {
    component.myForm.controls['exampleControl'].setValue('Test Value'); // Replace with your actual control name
    component.onSubmit(); // Call the submit method

    expect(component.myForm.valid).toBeTrue(); // Ensure the form is valid
    // Add additional expectations based on what your onSubmit method does
  });

  it('should render title in a h1 tag', () => {
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('h1').textContent).toContain('Your App Title'); // Replace with your actual title
  });

  // Add more tests as needed for your component's functionality
});

