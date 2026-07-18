<?php
/**
 * Standardized API response handler.
 *
 * @package SS_AI_Image_Search
 * @subpackage Api
 */

declare( strict_types=1 );

namespace SS_AI_Image_Search\Api;

use SS_AI_Image_Search\Exceptions\Api\ApiException;

/**
 * Response class for standardized API responses.
 */
class Response {

	/**
	 * Response status code.
	 *
	 * @var int
	 */
	private int $status_code;

	/**
	 * Response headers.
	 *
	 * @var array<string, string>
	 */
	private array $headers;

	/**
	 * Response body.
	 *
	 * @var array<string, mixed>
	 */
	private array $body;

	/**
	 * Constructor.
	 *
	 * @param int    $status_code HTTP status code.
	 * @param array  $body Response body data.
	 * @param array  $headers Response headers.
	 */
	public function __construct( int $status_code = 200, array $body = array(), array $headers = array() ) {
		$this->status_code = $status_code;
		$this->body        = $body;
		$this->headers     = $headers;
	}

	/**
	 * Create a successful response.
	 *
	 * @param mixed $data Response data.
	 * @param int   $status_code HTTP status code. Default 200.
	 * @return self
	 */
	public static function success( $data = null, int $status_code = 200 ): self {
		$body = array(
			'success' => true,
			'data'    => $data,
		);

		return new self( $status_code, $body );
	}

	/**
	 * Create an error response.
	 *
	 * @param string $message Error message.
	 * @param int    $status_code HTTP status code. Default 400.
	 * @param array  $errors Additional error details.
	 * @return self
	 */
	public static function error( string $message, int $status_code = 400, array $errors = array() ): self {
		$body = array(
			'success' => false,
			'message' => $message,
			'errors'  => $errors,
		);

		return new self( $status_code, $body );
	}

	/**
	 * Create a response from an exception.
	 *
	 * @param ApiException $exception Exception instance.
	 * @return self
	 */
	public static function from_exception( ApiException $exception ): self {
		$body = array(
			'success' => false,
			'message' => $exception->getMessage(),
			'errors'  => array(
				'code'    => $exception->get_code(),
				'context' => $exception->get_context(),
			),
		);

		return new self( $exception->get_http_status_code(), $body );
	}

	/**
	 * Create a response from WordPress HTTP API response.
	 *
	 * @param array $wp_response WordPress HTTP API response.
	 * @return self
	 */
	public static function from_wp_response( array $wp_response ): self {
		$status_code = wp_remote_retrieve_response_code( $wp_response );
		$body        = json_decode( wp_remote_retrieve_body( $wp_response ), true );
		$headers     = wp_remote_retrieve_headers( $wp_response );

		if ( ! is_array( $body ) ) {
			$body = array( 'raw_body' => wp_remote_retrieve_body( $wp_response ) );
		}

		return new self( $status_code, $body, $headers->getAll() );
	}

	/**
	 * Get the status code.
	 *
	 * @return int HTTP status code.
	 */
	public function get_status_code(): int {
		return $this->status_code;
	}

	/**
	 * Set the status code.
	 *
	 * @param int $status_code HTTP status code.
	 * @return void
	 */
	public function set_status_code( int $status_code ): void {
		$this->status_code = $status_code;
	}

	/**
	 * Get the response body.
	 *
	 * @return array<string, mixed> Response body.
	 */
	public function get_body(): array {
		return $this->body;
	}

	/**
	 * Set the response body.
	 *
	 * @param array<string, mixed> $body Response body.
	 * @return void
	 */
	public function set_body( array $body ): void {
		$this->body = $body;
	}

	/**
	 * Get a specific body field.
	 *
	 * @param string $key Field key.
	 * @param mixed  $default Default value if key not found.
	 * @return mixed Field value.
	 */
	public function get_field( string $key, $default = null ) {
		return $this->body[ $key ] ?? $default;
	}

	/**
	 * Get the response headers.
	 *
	 * @return array<string, string> Response headers.
	 */
	public function get_headers(): array {
		return $this->headers;
	}

	/**
	 * Set response headers.
	 *
	 * @param array<string, string> $headers Response headers.
	 * @return void
	 */
	public function set_headers( array $headers ): void {
		$this->headers = $headers;
	}

	/**
	 * Add a response header.
	 *
	 * @param string $name Header name.
	 * @param string $value Header value.
	 * @return void
	 */
	public function add_header( string $name, string $value ): void {
		$this->headers[ $name ] = $value;
	}

	/**
	 * Check if response is successful.
	 *
	 * @return bool True if status code is 2xx.
	 */
	public function is_successful(): bool {
		return $this->status_code >= 200 && $this->status_code < 300;
	}

	/**
	 * Check if response is an error.
	 *
	 * @return bool True if status code is 4xx or 5xx.
	 */
	public function is_error(): bool {
		return $this->status_code >= 400;
	}

	/**
	 * Convert response to array.
	 *
	 * @return array<string, mixed> Response as array.
	 */
	public function to_array(): array {
		return array(
			'status_code' => $this->status_code,
			'headers'     => $this->headers,
			'body'        => $this->body,
		);
	}

	/**
	 * Convert response to JSON.
	 *
	 * @return string JSON representation.
	 */
	public function to_json(): string {
		return wp_json_encode( $this->to_array() );
	}

	/**
	 * Get the success flag from body.
	 *
	 * @return bool Success flag.
	 */
	public function get_success(): bool {
		return $this->body['success'] ?? false;
	}

	/**
	 * Get the message from body.
	 *
	 * @return string Message.
	 */
	public function get_message(): string {
		return $this->body['message'] ?? '';
	}

	/**
	 * Get the data from body.
	 *
	 * @return mixed Response data.
	 */
	public function get_data() {
		return $this->body['data'] ?? null;
	}

	/**
	 * Get errors from body.
	 *
	 * @return array<string, mixed> Errors array.
	 */
	public function get_errors(): array {
		return $this->body['errors'] ?? array();
	}
}